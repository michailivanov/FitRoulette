from django.contrib import admin
from . import models

admin.site.register(models.CardSet)
admin.site.register(models.Exercise)
admin.site.register(models.GameSession)
admin.site.register(models.GameAdmin)
