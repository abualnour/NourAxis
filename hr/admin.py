from django.contrib import admin

from .models import HRAnnouncement, HRPolicy


@admin.register(HRPolicy)
class HRPolicyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "company", "effective_date", "is_active")
    list_filter = ("category", "is_active", "company")
    search_fields = ("title", "description", "company__name")


@admin.register(HRAnnouncement)
class HRAnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "published_at", "is_active")
    list_filter = ("audience", "is_active")
    search_fields = ("title", "message")
