# Generated by Django 4.0.2 on 2022-04-27 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_assigned', '0005_alter_working_duration_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='working_duration',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
