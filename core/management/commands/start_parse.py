from django.core.management import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore

from core.tasks import parse_queue_items


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            parse_queue_items,
            "interval",
            seconds=1,
            max_instances=3,
            id="fetch_queued_pages",
            replace_existing=True,
            jobstore="default"
        )
        scheduler.start()
