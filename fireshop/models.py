from django.db import models

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField(default=timezone.now())

class ShopPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ammount = models.IntegerField()
    last_updated_date = models.DateTimeField(auto_now=True)

class ShopPointsHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ammount = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

class ShopItem(models.Model):
