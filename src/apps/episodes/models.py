from django.conf import settings
from django.db import models


class Episode(models.Model):
    title = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    #link_to_episode??  # only if public?

    def __str__(self):
        return "RBR: {}".format(self.title)


class Notes(models.Model):
    episode = models.ForeignKey(Episode, related_name="notes")
    text = models.TextField()
    episode_timestamp = models.CharField(max_length=12, null=True, blank=True)  # 15:30, 15m 30s, 1530
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notes")

    def __str__(self):
        return "Notes for {}".format(self.episode.title)


class Character(models.Model):
    is_fool = models.BooleanField(default=False)
    name = models.CharField(max_length=64)


class CharacterAppearance(models.Model):
    character = models.ForeignKey(Character, related_name="episodes")
    episode = models.ForeignKey(Episode, related_name="characters")
