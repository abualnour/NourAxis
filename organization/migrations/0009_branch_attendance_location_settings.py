from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0008_alter_branch_image_alter_company_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="branch",
            name="attendance_latitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="branch",
            name="attendance_longitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="branch",
            name="attendance_radius_meters",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Allowed attendance radius in meters from the fixed branch point.",
                null=True,
            ),
        ),
    ]
