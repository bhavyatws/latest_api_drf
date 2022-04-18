# Generated by Django 4.0.2 on 2022-04-18 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('job_status', models.CharField(choices=[('New', 'New'), ('Progress', 'Progress'), ('Complete', 'Complete')], max_length=30)),
                ('job_deadline', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_associated', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job',
                'ordering': ('timestamp',),
            },
        ),
    ]
