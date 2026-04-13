from django.contrib import admin

from .models import (
    BranchScheduleGridCell,
    BranchScheduleGridHeader,
    BranchScheduleGridRow,
    BranchWeeklyDutyOption,
    BranchWeeklyPendingOff,
    BranchWeeklyScheduleEntry,
    Employee,
    EmployeeActionRecord,
    EmployeeAttendanceLedger,
    EmployeeLeave,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "full_name",
        "user",
        "company",
        "department",
        "branch",
        "section",
        "job_title",
        "hire_date",
        "is_active",
    )
    list_filter = (
        "is_active",
        "company",
        "department",
        "branch",
        "section",
        "job_title",
        "hire_date",
    )
    search_fields = (
        "employee_id",
        "full_name",
        "email",
        "phone",
        "user__email",
        "company__name",
        "department__name",
        "branch__name",
        "section__name",
        "job_title__name",
    )
    readonly_fields = ("employee_id", "created_at", "updated_at")
    list_select_related = (
        "user",
        "company",
        "department",
        "branch",
        "section",
        "job_title",
    )
    ordering = ("employee_id", "full_name")
    autocomplete_fields = (
        "user",
        "company",
        "department",
        "branch",
        "section",
        "job_title",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "employee_id",
                    "user",
                    "full_name",
                    "photo",
                    "email",
                    "phone",
                    "is_active",
                )
            },
        ),
        (
            "Organization Placement",
            {
                "fields": (
                    "company",
                    "department",
                    "branch",
                    "section",
                    "job_title",
                )
            },
        ),
        (
            "Employment Details",
            {
                "fields": (
                    "hire_date",
                    ("passport_issue_date", "passport_expiry_date"),
                    ("civil_id_issue_date", "civil_id_expiry_date"),
                    "salary",
                    "notes",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EmployeeLeave)
class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "start_date",
        "end_date",
        "total_days",
        "status",
        "requested_by",
        "approved_by",
        "created_at",
    )
    list_filter = (
        "leave_type",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )
    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "employee__user__email",
        "reason",
        "approval_note",
        "created_by",
        "updated_by",
    )
    readonly_fields = (
        "total_days",
        "created_at",
        "updated_at",
    )
    list_select_related = (
        "employee",
        "requested_by",
        "reviewed_by",
        "approved_by",
        "rejected_by",
        "cancelled_by",
    )
    autocomplete_fields = (
        "employee",
        "requested_by",
        "reviewed_by",
        "approved_by",
        "rejected_by",
        "cancelled_by",
    )
    ordering = ("-start_date", "-created_at")

    fieldsets = (
        (
            "Leave Information",
            {
                "fields": (
                    "employee",
                    "leave_type",
                    "status",
                    "start_date",
                    "end_date",
                    "total_days",
                )
            },
        ),
        (
            "Workflow Tracking",
            {
                "fields": (
                    "requested_by",
                    "reviewed_by",
                    "approved_by",
                    "rejected_by",
                    "cancelled_by",
                )
            },
        ),
        (
            "Notes",
            {
                "fields": (
                    "reason",
                    "approval_note",
                    "created_by",
                    "updated_by",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EmployeeActionRecord)
class EmployeeActionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "action_type",
        "action_date",
        "title",
        "status",
        "severity",
        "created_at",
    )
    list_filter = (
        "action_type",
        "status",
        "severity",
        "action_date",
        "created_at",
    )
    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "title",
        "description",
        "created_by",
        "updated_by",
    )
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("employee",)
    autocomplete_fields = ("employee",)
    ordering = ("-action_date", "-created_at")

    fieldsets = (
        (
            "Action Record",
            {
                "fields": (
                    "employee",
                    "action_type",
                    "action_date",
                    "title",
                    "description",
                    "status",
                    "severity",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EmployeeAttendanceLedger)
class EmployeeAttendanceLedgerAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "attendance_date",
        "day_status",
        "clock_in_time",
        "clock_out_time",
        "worked_hours",
        "late_minutes",
        "early_departure_minutes",
        "overtime_minutes",
        "is_paid_day",
        "source",
    )
    list_filter = (
        "day_status",
        "is_paid_day",
        "source",
        "attendance_date",
        "created_at",
    )
    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "notes",
        "created_by",
        "updated_by",
    )
    readonly_fields = (
        "worked_hours",
        "created_at",
        "updated_at",
    )
    list_select_related = (
        "employee",
        "linked_leave",
        "linked_action_record",
    )
    autocomplete_fields = (
        "employee",
        "linked_leave",
        "linked_action_record",
    )
    ordering = ("-attendance_date", "-created_at")

    fieldsets = (
        (
            "Attendance Entry",
            {
                "fields": (
                    "employee",
                    "attendance_date",
                    "day_status",
                    "clock_in_time",
                    "clock_out_time",
                    "scheduled_hours",
                    "worked_hours",
                    "late_minutes",
                    "early_departure_minutes",
                    "overtime_minutes",
                    "is_paid_day",
                    "source",
                )
            },
        ),
        (
            "Workflow Links",
            {
                "fields": (
                    "linked_leave",
                    "linked_action_record",
                    "notes",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(BranchWeeklyScheduleEntry)
class BranchWeeklyScheduleEntryAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_date",
        "branch",
        "employee",
        "title",
        "shift_label",
        "status",
        "updated_at",
    )
    list_filter = (
        "branch",
        "status",
        "week_start",
        "schedule_date",
    )
    search_fields = (
        "title",
        "shift_label",
        "order_note",
        "employee__full_name",
        "employee__employee_id",
        "branch__name",
    )
    readonly_fields = ("week_start", "created_at", "updated_at")
    list_select_related = ("branch", "employee")
    autocomplete_fields = ("branch", "employee", "duty_option")
    ordering = ("-schedule_date", "branch__name", "employee__full_name", "-id")


@admin.register(BranchWeeklyDutyOption)
class BranchWeeklyDutyOptionAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "branch",
        "duty_type",
        "default_start_time",
        "default_end_time",
        "display_order",
        "is_active",
    )
    list_filter = ("branch", "duty_type", "is_active")
    search_fields = ("label", "branch__name")
    list_select_related = ("branch",)
    autocomplete_fields = ("branch",)
    ordering = ("branch__name", "display_order", "label")


@admin.register(BranchWeeklyPendingOff)
class BranchWeeklyPendingOffAdmin(admin.ModelAdmin):
    list_display = ("week_start", "branch", "employee", "pending_off_count", "updated_at")
    list_filter = ("branch", "week_start")
    search_fields = ("employee__full_name", "employee__employee_id", "branch__name")
    list_select_related = ("branch", "employee")
    autocomplete_fields = ("branch", "employee")
    ordering = ("-week_start", "branch__name", "employee__full_name")


@admin.register(BranchScheduleGridCell)
class BranchScheduleGridCellAdmin(admin.ModelAdmin):
    list_display = ("branch", "row_index", "column_index", "updated_at")
    list_filter = ("branch", "column_index")
    search_fields = ("branch__name", "value")
    list_select_related = ("branch",)
    autocomplete_fields = ("branch",)
    ordering = ("branch__name", "row_index", "column_index")


@admin.register(BranchScheduleGridHeader)
class BranchScheduleGridHeaderAdmin(admin.ModelAdmin):
    list_display = ("branch", "column_index", "label", "updated_at")
    list_filter = ("branch",)
    search_fields = ("branch__name", "label")
    list_select_related = ("branch",)
    autocomplete_fields = ("branch",)
    ordering = ("branch__name", "column_index")


@admin.register(BranchScheduleGridRow)
class BranchScheduleGridRowAdmin(admin.ModelAdmin):
    list_display = ("branch", "row_index", "employee", "updated_at")
    list_filter = ("branch",)
    search_fields = ("branch__name", "employee__full_name", "employee__employee_id")
    list_select_related = ("branch", "employee")
    autocomplete_fields = ("branch", "employee")
    ordering = ("branch__name", "row_index")
