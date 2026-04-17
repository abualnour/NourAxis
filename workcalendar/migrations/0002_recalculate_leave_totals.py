from datetime import timedelta

from django.db import migrations


def recalculate_leave_totals(apps, schema_editor):
    EmployeeLeave = apps.get_model("employees", "EmployeeLeave")
    RegionalWorkCalendar = apps.get_model("workcalendar", "RegionalWorkCalendar")
    RegionalHoliday = apps.get_model("workcalendar", "RegionalHoliday")

    active_calendar = RegionalWorkCalendar.objects.filter(is_active=True).order_by("-updated_at", "-id").first()
    weekend_days = {4}
    if active_calendar and active_calendar.weekend_days:
        parsed_days = set()
        for raw_value in active_calendar.weekend_days.split(","):
            raw_value = raw_value.strip()
            if not raw_value:
                continue
            try:
                weekday_number = int(raw_value)
            except (TypeError, ValueError):
                continue
            if 0 <= weekday_number <= 6:
                parsed_days.add(weekday_number)
        if parsed_days:
            weekend_days = parsed_days

    holiday_dates = set()
    if active_calendar:
        holiday_dates = set(
            RegionalHoliday.objects.filter(calendar=active_calendar, is_non_working_day=True).values_list("holiday_date", flat=True)
        )

    for leave_record in EmployeeLeave.objects.all().iterator():
        if not leave_record.start_date or not leave_record.end_date or leave_record.end_date < leave_record.start_date:
            total_days = 0
        else:
            current_date = leave_record.start_date
            total_days = 0
            while current_date <= leave_record.end_date:
                if current_date.weekday() not in weekend_days and current_date not in holiday_dates:
                    total_days += 1
                current_date += timedelta(days=1)
        if leave_record.total_days != total_days:
            leave_record.total_days = total_days
            leave_record.save(update_fields=["total_days"])


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0036_delete_branchattendanceshiftsetting"),
        ("workcalendar", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(recalculate_leave_totals, migrations.RunPython.noop),
    ]
