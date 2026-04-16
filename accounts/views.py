from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from employees.access import get_workspace_profile_url
from employees.models import Employee
from config.session_timeout import (
    build_session_login_url,
    get_session_remaining_seconds,
    get_session_timeout_seconds,
    get_session_warning_seconds,
    set_session_last_activity,
)


class NourAxisLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        set_session_last_activity(self.request)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session_status"] = (self.request.GET.get("session") or "").strip().lower()
        return context

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        user = self.request.user
        employee = (
            Employee.objects.select_related("branch")
            .filter(user=user)
            .first()
        )
        if employee:
            return get_workspace_profile_url(user, employee)

        return get_workspace_profile_url(user, None)


@require_POST
def session_ping(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "timed_out": True,
                "login_url": build_session_login_url(next_url=request.POST.get("next", "")),
            },
            status=401,
        )

    set_session_last_activity(request)
    return JsonResponse(
        {
            "remaining_seconds": get_session_remaining_seconds(request),
            "timeout_seconds": get_session_timeout_seconds(),
            "warning_seconds": get_session_warning_seconds(),
        }
    )


@require_POST
def session_expire(request):
    if request.user.is_authenticated:
        logout(request)

    return JsonResponse(
        {
            "timed_out": True,
            "login_url": build_session_login_url(next_url=request.POST.get("next", "")),
        }
    )
