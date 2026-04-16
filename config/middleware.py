from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import resolve
from django.utils import timezone

from .session_timeout import (
    build_session_login_url,
    is_session_timed_out,
    set_session_last_activity,
)


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "user", None) and request.user.is_authenticated:
            current_view_name = self._get_view_name(request)
            now = timezone.now()

            if is_session_timed_out(request, now=now):
                return self._build_timeout_response(request, current_view_name)

            if self._should_refresh_activity(current_view_name):
                set_session_last_activity(request, now=now)

        return self.get_response(request)

    def _get_view_name(self, request):
        try:
            return resolve(request.path_info).view_name or ""
        except Exception:
            return ""

    def _should_refresh_activity(self, view_name):
        return view_name not in {"logout", "session_expire"}

    def _prefers_json(self, request, view_name):
        if view_name in {"session_ping", "session_expire"}:
            return True

        requested_with = request.headers.get("X-Requested-With", "")
        accept_header = request.headers.get("Accept", "")
        return requested_with == "XMLHttpRequest" or "application/json" in accept_header

    def _build_timeout_response(self, request, view_name):
        login_url = build_session_login_url(next_url=request.get_full_path())
        logout(request)

        if self._prefers_json(request, view_name):
            return JsonResponse(
                {
                    "timed_out": True,
                    "login_url": login_url,
                },
                status=401,
            )

        return redirect(login_url)
