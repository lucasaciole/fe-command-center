from django.db import models
from django.conf import settings

# Create your models here.
class FireRank(models.Model):
    name = models.CharField(max_length=100)
    points_reward = models.IntegerField()
    gems_reward = models.IntegerField()
    requirements_needed = models.IntegerField()

    def __str__(self):
    	return self.name

class FireRankRequirement(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
    	return self.description

class PlayerRank(models.Model):
    rank = models.ForeignKey(FireRank, on_delete=models.CASCADE)
    requirements_met = models.ManyToManyField(FireRankRequirement)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
    	return "{}: {}".format(self.user.username, self.rank.name)