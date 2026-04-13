from django.urls import path

from .views import hr_home

app_name = "hr"

urlpatterns = [
    path("", hr_home, name="home"),
]
