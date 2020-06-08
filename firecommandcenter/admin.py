from django.contrib import admin
from .models import Character, Class, ClassTree
# Register your models here.
admin.site.register(Class)
admin.site.register(Character)
admin.site.register(ClassTree)
