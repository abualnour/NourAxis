from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from accounts.views import NourAxisLoginView
from core.views import BackupCenterView, DashboardHomeView
from .views import system_landing

urlpatterns = [
    path("", system_landing, name="home"),
    path("dashboard/", DashboardHomeView.as_view(), name="dashboard_home"),
    path("system/backup-center/", BackupCenterView.as_view(), name="backup_center"),
    path("admin/", admin.site.urls),
    path("accounts/login/", NourAxisLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("organization/", include(("organization.urls", "organization"), namespace="organization")),
    path("employees/", include("employees.urls")),
]

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
