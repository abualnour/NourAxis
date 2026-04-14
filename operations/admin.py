from django.contrib import admin

from .models import BranchPost, BranchPostAcknowledgement, BranchPostReply, BranchTaskAction


@admin.register(BranchPost)
class BranchPostAdmin(admin.ModelAdmin):
    list_display = ("title", "branch", "post_type", "status", "priority", "is_pinned", "created_at")
    list_filter = ("branch", "post_type", "status", "priority", "is_pinned", "requires_acknowledgement")
    search_fields = ("title", "body", "branch__name", "author_employee__full_name", "assignee__full_name")
    autocomplete_fields = ("branch", "author_user", "author_employee", "assignee", "approved_by")


@admin.register(BranchPostReply)
class BranchPostReplyAdmin(admin.ModelAdmin):
    list_display = ("post", "author_employee", "created_at")
    search_fields = ("body", "post__title", "author_employee__full_name")
    autocomplete_fields = ("post", "author_user", "author_employee")


@admin.register(BranchTaskAction)
class BranchTaskActionAdmin(admin.ModelAdmin):
    list_display = ("post", "action_type", "actor_employee", "created_at")
    list_filter = ("action_type",)
    search_fields = ("post__title", "note", "actor_employee__full_name")
    autocomplete_fields = ("post", "actor_user", "actor_employee")


@admin.register(BranchPostAcknowledgement)
class BranchPostAcknowledgementAdmin(admin.ModelAdmin):
    list_display = ("post", "employee", "acknowledged_at")
    autocomplete_fields = ("post", "employee")
