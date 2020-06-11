from django.contrib import admin
from .models import Event, EventAttendanceCategory, PlayerPoints, PlayerPointsHistory, ShopItem

# Register your models here.
admin.site.register(Event)
admin.site.register(EventAttendanceCategory)
admin.site.register(PlayerPoints)
admin.site.register(PlayerPointsHistory)
admin.site.register(ShopItem)
