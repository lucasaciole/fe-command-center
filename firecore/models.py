from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class PlayerShop(models.Model):
    shop_type_choices = [
        ("FOOD", "Tenda de Comida"),
        ("BUFF", "Buffs de Pardoner"),
        ("WEPBUFF", "Buffs para Arma"),
        ("ENCHANT", "Enchants Peito e Calça"),
        ("AWAK", "Awakening"),
        ("ROAST", "Limpa Gemas"),
        ("SEX", "Troca de Sexo"),
        ("REPLEATHER", "Repair de Leather"),
        ("REPCLOTH", "Repair de Cloth"),
        ("REPPLATE", "Repair de Plate"),
        ("REPAIR", "Repair sem Arts")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_type = models.CharField(max_length=100, choices=shop_type_choices)
    location = models.CharField(max_length=100)

class ClassTree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Class(models.Model):
    class_tree = models.ForeignKey(ClassTree, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"

class Character(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_gtw_char = models.BooleanField(default=True)
    is_boruta_char = models.BooleanField(default=True)
    class_tree = models.ForeignKey(ClassTree, on_delete=models.SET_NULL, null=True, related_name='+')
    first_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='+')
    second_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='+')
    third_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='+')
    build_type = models.CharField(max_length = 100, null=True, choices = [
            ("CTR", "Controle"),
            ("DPS", "Dano"),
            ("SUP", "Suporte"),
            ("TNK", "Tanque"),
        ])

    def __str__(self):
        return "{self.user} {self.name}: {self.class_tree}/{self.first_class}/{self.second_class}/{self.third_class}".format(self = self)
