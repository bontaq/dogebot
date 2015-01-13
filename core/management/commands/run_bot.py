import logging
from django.core.management.base import BaseCommand
from core.soundcloud_api import SoundCloudAPI
from core.processing import Processor


logger = logging.getLogger('commands')


class Command(BaseCommand):
    help = 'Updates soundcloud, processes all messages, mentions, and transactions'

    def handle(self, *args, **options):
        soundcloud = SoundCloudAPI()
        processor = Processor()
        logger.info('beginning update')
        logger.info('beginning update soundcloud')
        soundcloud.update_soundcloud()
        logger.info('finished updating soundcloud')
        logger.info('beginning process messages')
        processor.process_messages()
        logger.info('finished process messages')
        logger.info('beginning process mentions')
        processor.process_mentions()
        logger.info('finished process mentions')
        logger.info('beginning process transactions')
        processor.process_transactions()
        logger.info('finished process transactions')
        logger.info('beginning process deposits')
        processor.process_deposits()
        logger.info('finished process deposits')
        logger.info('completed update')
