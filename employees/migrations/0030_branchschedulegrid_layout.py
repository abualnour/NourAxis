from django.db import migrations, models
import django.db.models.deletion


def migrate_branch_schedule_grid_cells(apps, schema_editor):
    BranchScheduleGridCell = apps.get_model("employees", "BranchScheduleGridCell")
    BranchScheduleGridRow = apps.get_model("employees", "BranchScheduleGridRow")

    branch_employee_pairs = []
    seen_pairs = set()

    existing_cells = BranchScheduleGridCell.objects.select_related("employee").order_by(
        "branch_id",
        "employee__full_name",
        "employee__employee_id",
        "column_index",
        "id",
    )

    for cell in existing_cells:
        pair = (cell.branch_id, cell.employee_id)
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            branch_employee_pairs.append(pair)

    row_map = {}
    branch_row_counters = {}

    for branch_id, employee_id in branch_employee_pairs:
        next_row_index = branch_row_counters.get(branch_id, 0) + 1
        branch_row_counters[branch_id] = next_row_index
        row_record = BranchScheduleGridRow.objects.create(
            branch_id=branch_id,
            row_index=next_row_index,
            employee_id=employee_id,
        )
        row_map[(branch_id, employee_id)] = row_record.row_index

    for cell in existing_cells:
        cell.row_index = row_map.get((cell.branch_id, cell.employee_id), 1)
        cell.save(update_fields=["row_index"])


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0029_branchschedulegridcell"),
        ("organization", "0008_alter_branch_image_alter_company_logo"),
    ]

    operations = [
        migrations.CreateModel(
            name="BranchScheduleGridHeader",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("column_index", models.PositiveSmallIntegerField()),
                ("label", models.CharField(blank=True, max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedule_grid_headers",
                        to="organization.branch",
                    ),
                ),
            ],
            options={
                "ordering": ["column_index", "id"],
                "unique_together": {("branch", "column_index")},
            },
        ),
        migrations.CreateModel(
            name="BranchScheduleGridRow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("row_index", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedule_grid_rows",
                        to="organization.branch",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_schedule_grid_rows",
                        to="employees.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["row_index", "id"],
                "unique_together": {("branch", "row_index")},
            },
        ),
        migrations.AddField(
            model_name="branchschedulegridcell",
            name="row_index",
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_branch_schedule_grid_cells, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name="branchschedulegridcell",
            unique_together={("branch", "row_index", "column_index")},
        ),
        migrations.RemoveField(
            model_name="branchschedulegridcell",
            name="employee",
        ),
        migrations.AlterModelOptions(
            name="branchschedulegridcell",
            options={"ordering": ["row_index", "column_index", "id"]},
        ),
    ]
