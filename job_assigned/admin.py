from django.contrib import admin
from job_assigned.models import JobAssigned,WorkingDuration

# Register your models here.
admin.site.register((JobAssigned,WorkingDuration))