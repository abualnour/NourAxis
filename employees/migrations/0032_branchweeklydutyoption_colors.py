from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0031_attendance_map_location_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="branchweeklydutyoption",
            name="background_color",
            field=models.CharField(blank=True, default="", max_length=7),
        ),
        migrations.AddField(
            model_name="branchweeklydutyoption",
            name="text_color",
            field=models.CharField(blank=True, default="", max_length=7),
        ),
    ]
