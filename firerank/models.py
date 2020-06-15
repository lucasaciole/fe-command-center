from django.db import models
from django.conf import settings

# Create your models here.
class FireRank(models.Model):
    name = models.CharField(max_length=100)
    points_reward = models.IntegerField()
    gems_reward = models.IntegerField()
    requirements_needed = models.IntegerField()

class FireRankRequirement(models.Model):
    description = models.CharField(max_length=100)

class PlayerRank(models.Model):
    rank = models.ForeignKey(FireRank, on_delete=models.CASCADE)
    requirements_met = models.ManyToManyField(FireRankRequirement)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)