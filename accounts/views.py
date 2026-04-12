from django.contrib.auth.views import LoginView
from django.urls import reverse

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
            return reverse("employees:self_service_profile")

        return reverse("home")
