# Generated by Django 4.0.2 on 2022-04-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_remove_job_worked_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_deadline',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
