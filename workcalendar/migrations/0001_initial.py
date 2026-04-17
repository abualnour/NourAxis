from django.db import migrations, models


def create_default_work_calendar(apps, schema_editor):
    RegionalWorkCalendar = apps.get_model("workcalendar", "RegionalWorkCalendar")
    if not RegionalWorkCalendar.objects.filter(is_active=True).exists():
        RegionalWorkCalendar.objects.create(
            name="Kuwait Government Work Calendar",
            region_code="KW",
            weekend_days="4",
            is_active=True,
            notes="System-wide Kuwait calendar with Friday configured as the weekly off day. Add official public holiday dates from the calendar workspace as they are confirmed.",
        )


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RegionalWorkCalendar",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Kuwait Government Work Calendar", max_length=150)),
                ("region_code", models.CharField(default="KW", max_length=10)),
                ("weekend_days", models.CharField(default="4", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Regional Work Calendar",
                "verbose_name_plural": "Regional Work Calendars",
                "ordering": ["-is_active", "name", "-id"],
            },
        ),
        migrations.CreateModel(
            name="RegionalHoliday",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("holiday_date", models.DateField(db_index=True)),
                ("title", models.CharField(max_length=160)),
                ("holiday_type", models.CharField(choices=[("public", "Public Holiday"), ("observance", "Official Observance")], default="public", max_length=20)),
                ("is_non_working_day", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("calendar", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="holidays", to="workcalendar.regionalworkcalendar")),
            ],
            options={
                "ordering": ["holiday_date", "title", "id"],
                "unique_together": {("calendar", "holiday_date", "title")},
            },
        ),
        migrations.RunPython(create_default_work_calendar, migrations.RunPython.noop),
    ]
