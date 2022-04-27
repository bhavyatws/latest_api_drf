from django.contrib import admin
from job_assigned.models import JobAssigned,Working_Duration

# Register your models here.
admin.site.register((JobAssigned,Working_Duration))