from django.contrib import admin

from . import models


admin.site.register(models.Character)
admin.site.register(models.CharacterAppearance)
admin.site.register(models.Episode)
admin.site.register(models.Notes)
