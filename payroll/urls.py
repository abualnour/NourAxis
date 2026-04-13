from django.urls import path

from .views import payroll_home, payroll_line_payslip, payroll_period_detail

app_name = "payroll"

urlpatterns = [
    path("", payroll_home, name="home"),
    path("periods/<int:pk>/", payroll_period_detail, name="period_detail"),
    path("lines/<int:pk>/payslip/", payroll_line_payslip, name="line_payslip"),
]
