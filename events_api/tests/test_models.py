from django.test import TestCase
from django.utils import timezone

from events_api.models import Event
from events_api.models import Track
from events_api.models import Team
from events_api.models import Rider
from events_api.models import RaceData
from events_api.models import EventWeatherConditions
from events_api.models import EventGeospatialData
from events_api.models import UciPoints


class BasicSetupTestCase(TestCase):
    """ Setup for testing default models logic and correctness """

    def setUp(self) -> None:
        start_date = timezone.now()
        end_date = timezone.now().replace(day=start_date.day + 2)

        self.event1 = Event.objects.create(
            event_title='DH-Race',
            event_type='DH',
            location='England',
            is_uci_regulated=True,
            start_date=start_date,
            end_date=end_date,
            stages=0,
            difficulty=8,
            event_weight=1.2
        )

        self.event2 = Event.objects.create(
            event_title='XC-Race',
            event_type='XC',
            location='Poland',
            is_uci_regulated=False,
            start_date=start_date,
            end_date=end_date,
            stages=0,
            difficulty=8,
            event_weight=1.2
        )

        self.track1 = Track.objects.create(
            event=self.event1,
            track_name='DH-Track-Eng',
            stage_number=0,
            track_length_meters=3_000,
        )

        self.track2 = Track.objects.create(
            event=self.event2,
            track_name='XC-Track-Pol',
            stage_number=0,
            track_length_meters=30_000,
        )

        self.team1 = Team.objects.create(
            team_name='Trek',
        )

        self.team2 = Team.objects.create(
            team_name='Cannondale',
        )

        self.rider1 = Rider.objects.create(
            first_name="John",
            last_name="Doe",
            age=27,
            country='England',
            team=self.team1,
            uci_points_total=1_000,
        )

        self.rider2 = Rider.objects.create(
            first_name="Jan",
            last_name="Kowalski",
            age=24,
            country='Poland',
            team=self.team2,
            uci_points_total=0,
        )

    def tearDown(self) -> None:
        Event.objects.all().delete()
        Track.objects.all().delete()
        Team.objects.all().delete()
        Rider.objects.all().delete()


class BasicModelTests(BasicSetupTestCase):

    def test_is_object_in_db(self):
        self.assertTrue(any(Event.objects.filter(event_title='DH-Race')))
        self.assertTrue(any(Event.objects.filter(event_title='XC-Race')))
        self.assertTrue(any(Track.objects.filter(track_name='XC-Track-Pol')))
        self.assertTrue(any(Team.objects.filter(team_name='Trek')))
        self.assertTrue(any(Rider.objects.filter(first_name='Jan')))

    def test_foreign_keys(self):
        rider1_country_name = self.rider1.country
        rider1_team_name = self.rider1.team.team_name
        self.assertEqual(rider1_country_name, "England")
        self.assertEqual(rider1_team_name, 'Trek')

        track1_event_title = self.track1.event.event_title
        self.assertEqual(track1_event_title, "DH-Race")

# TODO: Finish rest of model tests + API CRUDE and testing
