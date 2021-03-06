# Generated by Django 4.0.2 on 2022-04-28 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_assigned", "0004_remove_jobassigned_duration_worked_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="working_duration",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="working_duration",
            name="duration",
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="working_duration",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="working_duration",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
