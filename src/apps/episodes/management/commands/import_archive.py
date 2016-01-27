import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from dateutil import parser

from episodes.models import Episode, Character, CharacterAppearance, Notes


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Episode.objects.all().delete()

        admin = User.objects.get(pk=1)

        data = json.loads(open("src/scraping/archive_show_notes.json").read())
        for title, show_details in data.items():
            if not Episode.objects.filter(title=title).exists():
                print("Adding episode", title)
                episode = Episode.objects.create(
                    title=title,
                    date=parser.parse(show_details['date'])
                )
                Notes.objects.create(
                    episode=episode,
                    user=admin,
                    text=show_details["notes"]
                )

        # print(data)
