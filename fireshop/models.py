from django.db import models
from django.utils import timezone
from django.conf import settings
from firecore.models import Character
from django.db.models import F
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    has_party_planning = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.name,
                              self.date.date().strftime("%d/%m/%Y"))

class AttendanceTypes(models.TextChoices):
    GOING =  'going', _("Sim"),
    MAYBE =  'maybe', _("Talvez"),
    NOTGOING =  'notgoing', _("Não"),

class EventAttendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    attendance_type = models.CharField(max_length=100, choices=AttendanceTypes.choices)
    creation_date = models.DateTimeField(auto_now_add=True)
    confirmation_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.user.username, AttendanceTypes[self.attendance_type.upper()].label)

    def confirm(self, category):
        if self.confirmation_date is None:
            point_history_entry = PlayerPointHistory(user=self.user,
                                  amount_points= category.points_amount)
            point_history_entry.description = "{category}"


class EventAttendanceCategory(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_categories')
    points_amount = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(self.event.name, self.name)

    class Meta:
        verbose_name_plural = "Event Attendance Categories"

class EventAttendanceConfirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_category = models.ForeignKey(EventAttendanceCategory,
                                            on_delete=models.CASCADE)

class PlayerPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='shop_points')
    amount = models.IntegerField()
    last_updated_date = models.DateTimeField(auto_now=True)

    def add(self, value):
        self.amount = F('amount') + value
        self.save()

    def __str__(self):
        return "{}: {} ponto(s).".format(self.user.username, self.amount)

class PlayerPointsHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount_points = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_points()

    def update_user_points(self):
        try:
            if hasattr(self.user, 'shop_points'):
                self.user.shop_points.add(self.amount_points)
            else:
                shop_points = PlayerPoints(user=self.user, amount=self.amount_points)
                shop_points.save()
        except:
            self.delete()

    def __str__(self):
        return "{}: {}".format(self.user.username, self.description)

class ShopItem(models.Model):
    SHOP_ITEM_IMAGE_FOLDER = 'shop_items/'

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=SHOP_ITEM_IMAGE_FOLDER)
    points_cost = models.IntegerField()

class ShopItemRedeem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    additional_notes = models.CharField(max_length=100)

    def confirm(self):
        user_points = user.player_points

class EventParty(models.Model):
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    party_number = models.IntegerField()
    first_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    second_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    third_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    fourth_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')
    fifth_character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, related_name='+')