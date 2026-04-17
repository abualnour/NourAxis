from django.urls import path

from .views import work_calendar_home


app_name = "workcalendar"

urlpatterns = [
    path("", work_calendar_home, name="home"),
]

