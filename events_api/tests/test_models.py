from django.test import TestCase
from django.utils import timezone

from events_api.models import (
    Locations, Events
)


class TestEmpty(TestCase):

    def setUp(self) -> None:
        start_date = timezone.now()
        end_date = timezone.now().replace(day=start_date.day + 2)

        loc_pol = Locations.objects.create(
            country='Poland'
        )

        loc_eng = Locations.objects.create(
            country='England'
        )

        Events.objects.create(
            event_title='DH-Race',
            event_type='DH',
            location=loc_eng,
            is_uci_regulated=True,
            start_date=start_date,
            end_date=end_date,
            number_of_riders=21,
            stages=0,
            difficulty=8,
            event_weight=1.2
        )

    def tearDown(self) -> None:
        Events.objects.all().delete()
        Locations.objects.all().delete()

    def test_is_object_in_db(self):
        self.assertTrue(any(Events.objects.filter(event_title='DH-Race')))


