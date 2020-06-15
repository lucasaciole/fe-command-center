from django.contrib import admin
from . import models

# Register your models hmodels.ere.
admin.site.register(models.Event)
admin.site.register(models.EventAttendance)
admin.site.register(models.EventAttendanceCategory)
admin.site.register(models.PlayerPoints)
admin.site.register(models.PlayerPointsHistory)
admin.site.register(models.ShopItem)
