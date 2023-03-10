from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from events_api.models import Event
from events_api.models import Track
from events_api.models import Team
from events_api.models import Rider
from events_api.models import EventParticipant
from events_api.models import RaceData
from events_api.models import EventWeatherConditions
from events_api.models import EventGeospatialData
from events_api.models import UciPoints
from events_api.views import EventDetail


START_DATE: timezone = timezone.now().date()
END_TIME_PARAMS: dict = {
    'day': START_DATE.day + 2,
    'month': START_DATE.month,
    'year': START_DATE.year
}
END_DATE: timezone = timezone.now().date().replace(day=END_TIME_PARAMS['day'])


events_data: list = [
    {
        "event_title": "TestEvent1",
        "event_type": "DH",
        "location": "POL",
        "is_uci_regulated": False,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "stages": 0,
        "difficulty": "JR",
        "event_weight": 0.8,
    },
    {
        "event_title": "TestEvent2",
        "event_type": "XC",
        "location": "POL",
        "is_uci_regulated": False,
        "start_date": "2022-05-30",
        "end_date": "2022-05-30",
        "stages": 0,
        "difficulty": "SR",
        "event_weight": 1.5,
    },
    {
        "event_title": "TestEvent3",
        "event_type": "XC",
        "location": "POL",
        "is_uci_regulated": False,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "stages": 0,
        "difficulty": "SR",
        "event_weight": 2,
    },
    {
        "event_title": "TestEvent4",
        "event_type": "MT",
        "location": "CAN",
        "is_uci_regulated": False,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "stages": 1,
        "difficulty": "AM",
        "event_weight": 2.5,
    },
]

tracks_data: list = [
    {
        "track_name": "EasyTrack",
        "stage_number": 0,
        "track_length_meters": 5000,
    },
    {
        "track_name": "MediumTrack",
        "stage_number": 0,
        "track_length_meters": 5000,
    },
]

teams_data: list = [
    {
        "team_name": "Trek",
    },
    {
        "team_name": "Cannondale",
    },
]

riders_data: list = [
    {
        "first_name": "Jakub",
        "last_name": "Bagi??ski",
        "age": 24,
        "country": "Poland",
        "uci_points_total": 2000
    },
    {
        "first_name": "Test",
        "last_name": "User",
        "age": 27,
        "country": "Poland",
        "uci_points_total": 0
    }
]

race_data: list = [
    {
        "stage_time": "5:00",
        "position": 3,
    }
]

event_weather_data: list = [
    {
        "weather": "Sunshine",
        "avg_temp": 23.2,
        "avg_wind_speed": 15.10
    },
    {
        "weather": "Cloudy",
        "avg_temp": 11.5,
        "avg_wind_speed": 23
    }
]

event_location_data: list = [
    {
        "longitude": 54.397238,
        "latitude": 18.532388,
    },
    {
        "longitude": 54.514462,
        "latitude": 54.514462,
    }
]


class TestEventAPI(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='test')
        self.client.login(username='test_user', password='test')

        self.event1: Event = Event.objects.create(**events_data[0])
        self.track1: Track = Track.objects.create(event=self.event1, **tracks_data[0])

    def tearDown(self) -> None:
        User.objects.all().delete()
        Event.objects.all().delete()
        Track.objects.all().delete()
        Team.objects.all().delete()
        Rider.objects.all().delete()
        RaceData.objects.all().delete()

    def test_event_list_view(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_get(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post(self):
        url = reverse('event-list')
        data = dict(events_data[1])
        data["tracks"] = list()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.get(event_title=events_data[1]['event_title']).event_title, 'TestEvent2')

    def test_event_patch(self):
        url = reverse('event-list')
        data = dict(events_data[2])
        data['tracks'] = list()
        new_data = {
            "event_title": "test_event_patch_request",
            "event_type": "XC",
            "location": "POL",
            "is_uci_regulated": False,
            "start_date": "2022-02-14",
            "end_date": "2022-02-14",
            "stages": 0,
            "difficulty": "SR",
            "event_weight": 1.5,
        }

        response_post = self.client.post(url, data=events_data[2])
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        obj = Event.objects.get(event_title=events_data[2]['event_title'])
        url = reverse('event-detail', args=(obj.pk,))

        response_patch = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertNotEqual(events_data[2]["event_title"], new_data["event_title"])

    def test_event_put(self):
        url = reverse('event-list')
        data = dict(events_data[2])
        data['tracks'] = list()
        new_data = {
            "event_title": "test_event_put_request",
            "event_type": "CX",
            "location": "ENG",
            "is_uci_regulated": False,
            "start_date": "2022-02-14",
            "end_date": "2022-02-14",
            "stages": 1,
            "difficulty": "JR",
            "event_weight": 2.2,
        }

        response_post = self.client.post(url, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        obj = Event.objects.get(event_title=data['event_title'])
        url = reverse('event-detail', args=(obj.pk,))

        response_patch = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertNotEqual(data["event_title"], new_data["event_title"])

    def test_event_delete(self):
        get_pk = Event.objects.get(event_title=events_data[0]['event_title']).pk
        url = reverse('event-detail', args=(get_pk,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)


class TestTracksAPI(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='test')
        self.client.login(username='test_user', password='test')

        self.event1: Event = Event.objects.create(**events_data[0])
        self.track1: Track = Track.objects.create(event=self.event1, **tracks_data[0])

    def tearDown(self) -> None:
        User.objects.all().delete()
        Event.objects.all().delete()
        Track.objects.all().delete()

    def test_tracks_list_get(self):
        url = reverse('track-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_track_detail_get(self):
        data = tracks_data[1]

        Track.objects.create(event=self.event1, **data)
        obj = Track.objects.get(track_name='MediumTrack')
        get_pk = obj.pk

        url = reverse('track-detail', args=(get_pk,))
        response_get = self.client.get(url, data=obj.to_dict())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_track_post(self):
        data = tracks_data[1]

        Track.objects.create(event=self.event1, **data)
        obj = Track.objects.get(track_name='MediumTrack')

        url = reverse('track-list')
        response_post = self.client.post(url, data=obj.to_dict())
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

    def test_track_patch(self):
        data = tracks_data[1]

        Track.objects.create(event=self.event1, **data)
        obj = Track.objects.get(track_name='MediumTrack')

        url = reverse('track-detail', args=(obj.pk,))
        new_data = {"track_name": "NewTrackName"}

        response_patch = self.client.patch(url, data=new_data)
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

    def test_track_put(self):
        data = tracks_data[1]

        Track.objects.create(event=self.event1, **data)
        obj = Track.objects.get(track_name='EasyTrack')

        url = reverse('track-detail', args=(obj.pk,))
        new_data = {
            "track_name": "UpdatedTrackName",
            "stage_number": 1,
            "track_length_meters": 10000,
        }
        response_put = self.client.put(url, data=new_data)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)

    def test_track_delete(self):
        obj = Track.objects.get(track_name='EasyTrack')
        url = reverse('track-detail', args=(obj.pk,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)


class TestEventParticipantsAPI(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='test')
        self.client.login(username='test_user', password='test')

        self.event1: Event = Event.objects.create(**events_data[0])
        self.event2: Event = Event.objects.create(**events_data[1])
        self.event3: Event = Event.objects.create(**events_data[3])

        self.team1: Team = Team.objects.create(**teams_data[0])
        self.rider1: Rider = Rider.objects.create(team=self.team1, **riders_data[0])
        self.event_participant = EventParticipant.objects.create(person=self.rider1, event=self.event3)

    def tearDown(self) -> None:
        User.objects.all().delete()
        Event.objects.all().delete()
        Team.objects.all().delete()
        Rider.objects.all().delete()
        EventParticipant.objects.all().delete()

    def test_event_participants_get(self):
        url = reverse('event-participants-list')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_event_participants_post(self):
        obj_get_rider = Rider.objects.get(first_name='Jakub', last_name='Bagi??ski')
        obj_get_event = Event.objects.get(event_title='TestEvent1')
        data = {
            "person": obj_get_rider.pk,
            "event": obj_get_event.pk,
        }

        url = reverse('event-participants-list')
        response_post = self.client.post(url, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        get_pk = EventParticipant.objects.get(person=1, event=1).pk

        url = reverse('event-participants-detail', args=(get_pk,))
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_event_update(self):
        """ Both put and patch methods are handled by perform_update() """
        # Post new item
        obj_get_rider = Rider.objects.get(first_name='Jakub', last_name='Bagi??ski')
        obj_get_event = Event.objects.get(event_title='TestEvent1')
        data = {
            "person": obj_get_rider.pk,
            "event": obj_get_event.pk,
        }

        url = reverse('event-participants-list')
        response_post = self.client.post(url, data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        # Update data in record
        Rider.objects.create(
            team=self.team1,
            first_name='new',
            last_name='rider',
            age=18,
            country='Canada',
            uci_points_total=0,
        )
        new_rider_obj = Rider.objects.get(first_name='new', last_name='rider')
        new_data = {"person": new_rider_obj.pk}

        get_pk = EventParticipant.objects.get(person=1, event=1).pk

        url = reverse('event-participants-detail', args=(get_pk,))
        response_patch = self.client.patch(url, data=new_data)

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertTrue(EventParticipant.objects.get(pk=get_pk).to_dict().get('person'), new_rider_obj.pk)

        new_data["person"] = self.rider1.pk
        new_data["event"] = self.event2.pk

        response_patch = self.client.patch(url, data=new_data)

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertTrue(EventParticipant.objects.get(pk=get_pk).to_dict().get("person"), new_data["person"])
        self.assertTrue(EventParticipant.objects.get(pk=get_pk).to_dict().get("event"), new_data["event"])

    def test_event_participants_delete(self):
        obj = EventParticipant.objects.get(person=self.rider1.pk, event=self.event3)
        url = reverse('event-participants-detail', args=(obj.pk,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)


# TODO: Finish CRUDE tests for EventParticipants
