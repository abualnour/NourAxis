from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import timezone

from employees.access import (
    is_admin_compatible,
    is_branch_scoped_supervisor,
    is_hr_user,
    is_operations_manager_user,
)
from employees.models import BranchWeeklyScheduleEntry, Employee, get_schedule_week_start

from .models import BranchPost, BranchPostAcknowledgement, BranchTaskAction


def get_user_employee_profile(user):
    if not user or not user.is_authenticated:
        return None

    try:
        return user.employee_profile
    except Exception:
        return None


def can_access_branch_workspace(user, branch, employee=None):
    if not user or not user.is_authenticated or not branch:
        return False

    if is_admin_compatible(user) or is_hr_user(user) or is_operations_manager_user(user):
        return True

    linked_employee = employee or get_user_employee_profile(user)
    return bool(linked_employee and getattr(linked_employee, "branch_id", None) == branch.id)


def can_manage_branch_workspace(user, branch, employee=None):
    if not user or not user.is_authenticated or not branch:
        return False

    if is_admin_compatible(user) or is_hr_user(user) or is_operations_manager_user(user):
        return True

    linked_employee = employee or get_user_employee_profile(user)
    return bool(
        linked_employee
        and getattr(linked_employee, "branch_id", None) == branch.id
        and is_branch_scoped_supervisor(user, linked_employee)
    )


def can_create_branch_post(user, branch, employee=None):
    return can_access_branch_workspace(user, branch, employee=employee)


def can_reply_branch_post(user, post, employee=None):
    return bool(post and can_access_branch_workspace(user, post.branch, employee=employee))


def can_manage_branch_post(user, post, employee=None):
    return bool(post and can_manage_branch_workspace(user, post.branch, employee=employee))


def can_change_branch_post_status(user, post, target_status, employee=None):
    if not post or not target_status:
        return False

    linked_employee = employee or get_user_employee_profile(user)
    management_only_statuses = {
        BranchPost.STATUS_APPROVED,
        BranchPost.STATUS_REJECTED,
        BranchPost.STATUS_CLOSED,
    }

    if target_status in management_only_statuses:
        return can_manage_branch_post(user, post, employee=linked_employee)

    if can_manage_branch_post(user, post, employee=linked_employee):
        return True

    return bool(
        linked_employee
        and post.assignee_id == linked_employee.id
        and target_status in {
            BranchPost.STATUS_OPEN,
            BranchPost.STATUS_IN_PROGRESS,
            BranchPost.STATUS_DONE,
        }
    )


def can_acknowledge_branch_post(user, post, employee=None):
    linked_employee = employee or get_user_employee_profile(user)
    return bool(
        post
        and post.requires_acknowledgement
        and linked_employee
        and linked_employee.branch_id == post.branch_id
    )


def ensure_branch_access(user, branch, employee=None):
    if not can_access_branch_workspace(user, branch, employee=employee):
        raise PermissionDenied("You do not have permission to access this branch workspace.")


def get_branch_team_members(branch):
    if not branch:
        return []
    return list(
        Employee.objects.select_related("job_title", "section", "department")
        .filter(branch=branch, is_active=True)
        .order_by("full_name", "employee_id")
    )


def get_branch_post_queryset(branch):
    return BranchPost.objects.select_related(
        "branch",
        "author_user",
        "author_employee",
        "assignee",
        "assignee__job_title",
        "approved_by",
    ).prefetch_related("replies", "acknowledgements").filter(branch=branch, is_published=True)


def build_branch_post_cards(posts, *, employee=None):
    acknowledged_ids = set()
    if employee:
        acknowledged_ids = set(
            BranchPostAcknowledgement.objects.filter(
                employee=employee,
                post_id__in=[post.id for post in posts],
            ).values_list("post_id", flat=True)
        )

    cards = []
    today = timezone.localdate()
    for post in posts:
        cards.append(
            {
                "object": post,
                "detail_url": reverse("operations:branch_post_detail", kwargs={"post_id": post.id}),
                "reply_total": post.replies.count(),
                "ack_total": post.acknowledgements.count(),
                "assignee_label": post.assignee.full_name if post.assignee_id else "",
                "assignee_role_label": getattr(getattr(post.assignee, "job_title", None), "name", "") if post.assignee_id else "",
                "is_acknowledged": post.id in acknowledged_ids,
                "is_due_soon": bool(post.due_date and today <= post.due_date <= today + timedelta(days=2)),
                "is_overdue": bool(post.due_date and post.due_date < today and post.status not in {BranchPost.STATUS_APPROVED, BranchPost.STATUS_CLOSED}),
            }
        )
    return cards


def build_branch_workspace_context(branch, user, *, employee=None, week_start=None):
    ensure_branch_access(user, branch, employee=employee)
    selected_week_start = week_start or get_schedule_week_start(timezone.localdate())
    week_end = selected_week_start + timedelta(days=6)
    team_members = get_branch_team_members(branch)
    post_queryset = get_branch_post_queryset(branch)
    pinned_posts = list(post_queryset.filter(is_pinned=True)[:4])
    recent_posts = list(post_queryset[:8])
    schedule_entries = BranchWeeklyScheduleEntry.objects.filter(branch=branch, week_start=selected_week_start)

    return {
        "branch_workspace_branch": branch,
        "branch_workspace_selected_week_start": selected_week_start,
        "branch_workspace_week_end": week_end,
        "branch_workspace_team_members": team_members,
        "branch_workspace_team_total": len(team_members),
        "branch_workspace_pinned_posts": build_branch_post_cards(pinned_posts, employee=employee),
        "branch_workspace_recent_posts": build_branch_post_cards(recent_posts, employee=employee),
        "branch_workspace_open_task_total": post_queryset.filter(
            post_type__in=[BranchPost.POST_TYPE_TASK, BranchPost.POST_TYPE_ISSUE],
            status__in=[BranchPost.STATUS_OPEN, BranchPost.STATUS_IN_PROGRESS, BranchPost.STATUS_DONE],
        ).count(),
        "branch_workspace_approval_waiting_total": post_queryset.filter(
            post_type__in=[BranchPost.POST_TYPE_TASK, BranchPost.POST_TYPE_ISSUE],
            status=BranchPost.STATUS_DONE,
        ).count(),
        "branch_workspace_announcement_total": post_queryset.filter(post_type=BranchPost.POST_TYPE_ANNOUNCEMENT).count(),
        "branch_workspace_today_schedule_total": schedule_entries.filter(schedule_date=timezone.localdate()).count(),
        "can_create_branch_post": can_create_branch_post(user, branch, employee=employee),
        "can_manage_branch_workspace": can_manage_branch_workspace(user, branch, employee=employee),
    }


def format_schedule_entry_label(entry):
    if not entry:
        return "No schedule assigned for today"
    if entry.shift_label:
        return entry.shift_label
    if entry.duty_option_id:
        return entry.duty_option.label
    if entry.title:
        return entry.title
    return entry.get_duty_type_display()


def build_employee_schedule_snapshot(employee, *, reference_date=None):
    if not employee or not getattr(employee, "branch_id", None):
        return {
            "my_schedule_today_entry": None,
            "my_schedule_today_label": "",
            "my_schedule_this_week_entries": [],
            "my_schedule_next_week_entries": [],
            "my_schedule_this_week_start": None,
            "my_schedule_next_week_start": None,
        }

    today = reference_date or timezone.localdate()
    this_week_start = get_schedule_week_start(today)
    next_week_start = this_week_start + timedelta(days=7)
    next_week_end = next_week_start + timedelta(days=6)

    entries = list(
        BranchWeeklyScheduleEntry.objects.select_related("duty_option")
        .filter(
            employee=employee,
            branch=employee.branch,
            schedule_date__gte=this_week_start,
            schedule_date__lte=next_week_end,
        )
        .order_by("schedule_date", "id")
    )
    today_entry = next((entry for entry in entries if entry.schedule_date == today), None)

    return {
        "my_schedule_today_entry": today_entry,
        "my_schedule_today_label": format_schedule_entry_label(today_entry),
        "my_schedule_this_week_entries": [entry for entry in entries if this_week_start <= entry.schedule_date <= this_week_start + timedelta(days=6)],
        "my_schedule_next_week_entries": [entry for entry in entries if next_week_start <= entry.schedule_date <= next_week_end],
        "my_schedule_this_week_start": this_week_start,
        "my_schedule_next_week_start": next_week_start,
    }


def create_post_action(post, *, action_type, user=None, employee=None, note="", from_status="", to_status=""):
    return BranchTaskAction.objects.create(
        post=post,
        actor_user=user if getattr(user, "is_authenticated", False) else None,
        actor_employee=employee,
        action_type=action_type,
        note=note,
        from_status=from_status,
        to_status=to_status,
    )
