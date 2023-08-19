import datetime

from django.test import TestCase

from core.models import Community, ParsingQueue
from core.tasks import parse_queue_items


class TestQueueParsing(TestCase):
    def test_queue_parsing(self):
        community = Community.objects.create(
            link="https://vk.com/kirov_spb",
            category="общая",
            stat_start_time=datetime.datetime.now()
        )
        queue_item = ParsingQueue.objects.first()
        print(queue_item)
        parse_queue_items()
