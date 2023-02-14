from django.test import TestCase
from django.utils import timezone

from events_api.models import Locations
from events_api.models import Events
from events_api.models import Tracks
from events_api.models import Teams
from events_api.models import Riders
from events_api.models import RaceData
from events_api.models import EventWeatherConditions
from events_api.models import EventGeospatialData
from events_api.models import UciPoints


class BasicSetupTestCase(TestCase):
    """ Setup for testing default models logic and correctness """

    def setUp(self) -> None:
        start_date = timezone.now()
        end_date = timezone.now().replace(day=start_date.day + 2)

        loc_pol = Locations.objects.create(
            country='Poland'
        )

        loc_eng = Locations.objects.create(
            country='England'
        )

        self.event1 = Events.objects.create(
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

        self.event2 = Events.objects.create(
            event_title='XC-Race',
            event_type='XC',
            location=loc_pol,
            is_uci_regulated=False,
            start_date=start_date,
            end_date=end_date,
            number_of_riders=21,
            stages=0,
            difficulty=8,
            event_weight=1.2
        )

        self.track1 = Tracks.objects.create(
            event=self.event1,
            track_name='DH-Track-Eng',
            stage_number=0,
            track_length_meters=3_000,
        )

        self.track2 = Tracks.objects.create(
            event=self.event2,
            track_name='XC-Track-Pol',
            stage_number=0,
            track_length_meters=30_000,
        )

        self.team1 = Teams.objects.create(
            team_name='Trek',
        )

        self.team2 = Teams.objects.create(
            team_name='Cannondale',
        )

        self.rider1 = Riders.objects.create(
            first_name="John",
            last_name="Doe",
            age=27,
            country=loc_eng,
            team=self.team1,
            uci_points_total=1_000,
        )

        self.rider2 = Riders.objects.create(
            first_name="Jan",
            last_name="Kowalski",
            age=24,
            country=loc_pol,
            team=self.team2,
            uci_points_total=0,
        )

    def tearDown(self) -> None:
        Events.objects.all().delete()
        Locations.objects.all().delete()
        Tracks.objects.all().delete()
        Teams.objects.all().delete()
        Riders.objects.all().delete()


class BasicModelTests(BasicSetupTestCase):

    def test_is_object_in_db(self):
        self.assertTrue(any(Events.objects.filter(event_title='DH-Race')))
        self.assertTrue(any(Events.objects.filter(event_title='XC-Race')))
        self.assertTrue(any(Locations.objects.filter(country='Poland')))
        self.assertTrue(any(Tracks.objects.filter(track_name='XC-Track-Pol')))
        self.assertTrue(any(Teams.objects.filter(team_name='Trek')))
        self.assertTrue(any(Riders.objects.filter(first_name='Jan')))

    def test_foreign_keys(self):
        rider1_country_name = self.rider1.country.country
        rider1_team_name = self.rider1.team.team_name
        self.assertEqual(rider1_country_name, "England")
        self.assertEqual(rider1_team_name, 'Trek')

        track1_event_title = self.track1.event.event_title
        self.assertEqual(track1_event_title, "DH-Race")

# TODO: Finish rest of model tests + API CRUDE and testing
