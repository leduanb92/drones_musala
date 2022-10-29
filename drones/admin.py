from django.contrib import admin

from drones.models import Drone, Medication

# Register your models here.
admin.site.register(Drone)
admin.site.register(Medication)
