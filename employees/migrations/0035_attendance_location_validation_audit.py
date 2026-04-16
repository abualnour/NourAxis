from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0034_branchattendanceshiftsetting"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="attendance_radius_meters_used",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="branch_latitude_used",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="branch_longitude_used",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_in_distance_meters",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_in_location_validation_status",
            field=models.CharField(
                blank=True,
                choices=[("inside_radius", "Inside Radius"), ("outside_radius", "Outside Radius")],
                default="",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_out_distance_meters",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_out_location_validation_status",
            field=models.CharField(
                blank=True,
                choices=[("inside_radius", "Inside Radius"), ("outside_radius", "Outside Radius")],
                default="",
                max_length=20,
            ),
        ),
    ]
