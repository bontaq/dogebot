from django.core.management.base import BaseCommand, CommandError
from core.soundcloud_api import SoundCloudAPI
from core.processing import Processor


class Command(BaseCommand):
    help = 'Does everything we can currently do :D'

    def handle(self, *args, **options):
        processor = Processor()
        processor.soundcloud.update_soundcloud()
        processor.process_messages()
        processor.process_mentions()
