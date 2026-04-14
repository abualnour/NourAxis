from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0030_branchschedulegrid_layout"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_in_address",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="employeeattendanceevent",
            name="check_out_address",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_in_address",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_in_latitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_in_location_label",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_in_longitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_out_address",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_out_latitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_out_location_label",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="employeeattendanceledger",
            name="check_out_longitude",
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
