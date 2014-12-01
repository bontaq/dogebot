from django.core.management.base import BaseCommand
from core.soundcloud_api import SoundCloudAPI


class Command(BaseCommand):
    help = 'Creates new conversations from soundcloud'

    def handle(self, *args, **options):
        soundcloud = SoundCloudAPI()
        soundcloud.update_soundcloud()
        # soundcloud.create_conversations()
