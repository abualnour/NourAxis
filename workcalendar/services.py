from datetime import date, timedelta

from django.utils import timezone

from .models import RegionalHoliday, RegionalWorkCalendar


DEFAULT_WEEKEND_DAYS = {4}


def get_active_calendar():
    return (
        RegionalWorkCalendar.objects.filter(is_active=True)
        .prefetch_related("holidays")
        .order_by("-updated_at", "-id")
        .first()
    )


def get_policy_weekend_days():
    calendar = get_active_calendar()
    if not calendar:
        return set(DEFAULT_WEEKEND_DAYS)
    return calendar.weekend_day_numbers or set(DEFAULT_WEEKEND_DAYS)


def is_weekly_off_day(value):
    if not value:
        return False
    return value.weekday() in get_policy_weekend_days()


def get_holidays_for_range(start_date, end_date):
    if not start_date or not end_date or start_date > end_date:
        return []

    calendar = get_active_calendar()
    if not calendar:
        return []

    return list(
        RegionalHoliday.objects.filter(
            calendar=calendar,
            holiday_date__gte=start_date,
            holiday_date__lte=end_date,
        ).order_by("holiday_date", "title", "id")
    )


def get_non_working_holiday_dates(start_date, end_date):
    return {
        holiday.holiday_date
        for holiday in get_holidays_for_range(start_date, end_date)
        if holiday.is_non_working_day
    }


def get_holiday_for_date(value):
    if not value:
        return None
    calendar = get_active_calendar()
    if not calendar:
        return None
    return (
        RegionalHoliday.objects.filter(
            calendar=calendar,
            holiday_date=value,
        )
        .order_by("id")
        .first()
    )


def is_public_holiday(value):
    holiday = get_holiday_for_date(value)
    return bool(holiday and holiday.is_non_working_day)


def classify_day(value):
    holiday = get_holiday_for_date(value)
    if holiday and holiday.is_non_working_day:
        return {
            "code": "holiday",
            "label": holiday.title,
            "holiday": holiday,
        }
    if is_weekly_off_day(value):
        return {
            "code": "weekly_off",
            "label": "Weekly Off",
            "holiday": holiday,
        }
    return {
        "code": "working_day",
        "label": "Working Day",
        "holiday": holiday,
    }


def is_working_day(value):
    if not value:
        return False
    day_context = classify_day(value)
    return day_context["code"] == "working_day"


def count_working_days(start_date, end_date):
    if not start_date or not end_date or start_date > end_date:
        return 0

    non_working_holidays = get_non_working_holiday_dates(start_date, end_date)
    weekend_days = get_policy_weekend_days()
    current_date = start_date
    working_days = 0

    while current_date <= end_date:
        if current_date.weekday() not in weekend_days and current_date not in non_working_holidays:
            working_days += 1
        current_date += timedelta(days=1)

    return working_days


def build_work_calendar_overview(target_year=None):
    today = timezone.localdate()
    active_calendar = get_active_calendar()
    weekend_days = get_policy_weekend_days()
    year = target_year or today.year
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    holidays = get_holidays_for_range(year_start, year_end)
    non_working_holiday_dates = {
        holiday.holiday_date
        for holiday in holidays
        if holiday.is_non_working_day
    }
    weekly_off_dates = set()
    current_date = year_start
    while current_date <= year_end:
        if current_date.weekday() in weekend_days:
            weekly_off_dates.add(current_date)
        current_date += timedelta(days=1)
    combined_non_working_dates = weekly_off_dates | non_working_holiday_dates

    return {
        "active_calendar": active_calendar,
        "today_context": classify_day(today),
        "current_year": year,
        "holiday_total": len(holidays),
        "non_working_holiday_total": sum(1 for holiday in holidays if holiday.is_non_working_day),
        "observance_holiday_total": sum(1 for holiday in holidays if not holiday.is_non_working_day),
        "weekly_off_day_total": len(weekly_off_dates),
        "combined_non_working_day_total": len(combined_non_working_dates),
        "working_day_total": count_working_days(year_start, year_end),
        "weekly_off_days": sorted(weekend_days),
        "holidays": holidays,
    }


def recalculate_employee_leave_totals():
    from employees.models import EmployeeLeave

    updated_count = 0
    for leave_record in EmployeeLeave.objects.all().iterator():
        total_days = count_working_days(leave_record.start_date, leave_record.end_date)
        if leave_record.total_days != total_days:
            leave_record.total_days = total_days
            leave_record.save(update_fields=["total_days"])
            updated_count += 1
    return updated_count
