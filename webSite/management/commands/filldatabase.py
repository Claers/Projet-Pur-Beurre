from django.core.management.base import BaseCommand
from webSite.database_fill import fill_cron
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fill the database with 50 pages of OFF data"

    def handle(self, *args, **options):

        fill_cron_thread = fill_cron()
        fill_cron_thread.start()
        self.stdout.write(self.style.SUCCESS('Database filled with success'))
        logger.info('Database filled with success')
