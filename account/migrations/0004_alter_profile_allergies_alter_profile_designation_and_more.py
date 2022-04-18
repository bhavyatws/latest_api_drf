# Generated by Django 4.0.2 on 2022-04-15 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_certification_level_profile_certification_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='allergies',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='medical_issues',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]