from django.urls import path

from .views import (
    branch_post_acknowledge,
    branch_post_create,
    branch_post_detail,
    branch_post_reply_create,
    branch_post_status_update,
    branch_workspace_detail,
)

app_name = "operations"

urlpatterns = [
    path("branches/<int:branch_id>/workspace/", branch_workspace_detail, name="branch_workspace_detail"),
    path("branches/<int:branch_id>/posts/create/", branch_post_create, name="branch_post_create"),
    path("posts/<int:post_id>/", branch_post_detail, name="branch_post_detail"),
    path("posts/<int:post_id>/reply/", branch_post_reply_create, name="branch_post_reply_create"),
    path("posts/<int:post_id>/status/", branch_post_status_update, name="branch_post_status_update"),
    path("posts/<int:post_id>/acknowledge/", branch_post_acknowledge, name="branch_post_acknowledge"),
]
