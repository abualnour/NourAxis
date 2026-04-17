from django.contrib import admin

from .models import RegionalHoliday, RegionalWorkCalendar


@admin.register(RegionalWorkCalendar)
class RegionalWorkCalendarAdmin(admin.ModelAdmin):
    list_display = ("name", "region_code", "is_active", "weekend_days", "updated_at")
    list_filter = ("is_active", "region_code")
    search_fields = ("name", "region_code", "notes")


@admin.register(RegionalHoliday)
class RegionalHolidayAdmin(admin.ModelAdmin):
    list_display = ("title", "holiday_date", "calendar", "holiday_type", "is_non_working_day")
    list_filter = ("holiday_type", "is_non_working_day", "calendar")
    search_fields = ("title", "notes")

