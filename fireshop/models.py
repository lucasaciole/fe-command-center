from django.db import models
from django.utils import timezone
from django.conf import settings
from firecore.models import Character

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField(default=timezone.now)
    has_party_planning = models.BooleanField(default=True)

    def __str__(self):
        return self.event_name

class EventAttendance(models.Model):
    attendance_type_choices = [
        ("Y", "Sim"),
        ("M", "Talvez"),
        ("N", "Não"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_type = models.CharField(max_length=100, choices=attendance_type_choices)


class EventAttendanceCategory(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    points_ammount = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(self.event.event_name, self.name)

    class Meta:
        verbose_name_plural = "Event Attendance Categories"

class EventAttendanceConfirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_category = models.ForeignKey(EventAttendanceCategory, on_delete=models.CASCADE)

class PlayerPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ammount = models.IntegerField()
    last_updated_date = models.DateTimeField(auto_now=True)

class PlayerPointsHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_attendance_category = models.ForeignKey(EventAttendanceCategory, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

class ShopItem(models.Model):
    SHOP_ITEM_IMAGE_FOLDER = 'shop_items/'

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=SHOP_ITEM_IMAGE_FOLDER)
    points_ammount = models.IntegerField()

class ShopItemRedeem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    additional_notes = models.CharField(max_length=100)

class EventParty(models.Model):
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    party_number = models.IntegerField()
    first_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    second_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    third_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    fourth_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    fifth_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')