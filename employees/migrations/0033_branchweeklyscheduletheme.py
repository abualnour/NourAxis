from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0032_branchweeklydutyoption_colors"),
    ]

    operations = [
        migrations.CreateModel(
            name="BranchWeeklyScheduleTheme",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_column_bg", models.CharField(blank=True, default="#101828", max_length=7)),
                ("employee_column_text", models.CharField(blank=True, default="#f8fafc", max_length=7)),
                ("job_title_column_bg", models.CharField(blank=True, default="#111827", max_length=7)),
                ("job_title_column_text", models.CharField(blank=True, default="#f8fafc", max_length=7)),
                ("pending_off_column_bg", models.CharField(blank=True, default="#172033", max_length=7)),
                ("pending_off_column_text", models.CharField(blank=True, default="#f8fafc", max_length=7)),
                ("day_header_bg", models.CharField(blank=True, default="#1d293d", max_length=7)),
                ("day_header_text", models.CharField(blank=True, default="#f8fafc", max_length=7)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("branch", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="weekly_schedule_theme", to="organization.branch")),
            ],
            options={
                "ordering": ["branch__name"],
            },
        ),
    ]
