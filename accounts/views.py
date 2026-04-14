from django.contrib.auth.views import LoginView

from employees.access import get_workspace_profile_url
from employees.models import Employee


class NourAxisLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

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
