from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from events_api.models import Events
from events_api.models import Tracks
from events_api.models import Teams
from events_api.models import Riders
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
        "number_of_riders": 18,
        "stages": 0,
        "difficulty": "JR",
        "event_weight": 0.8,
    },
    {
        "event_title": "TestEvent2",
        "event_type": "XC",
        "location": "POL",
        "is_uci_regulated": False,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "number_of_riders": 18,
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
        "number_of_riders": 15,
        "stages": 0,
        "difficulty": "SR",
        "event_weight": 2,
    },
]

tracks_data: list = [
    {
        "track_name": "EasyTrack",
        "stage_number": 0,
        "track_length_meters": 5_000,
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
        "last_name": "Bagiński",
        "age": 24,
        "country": "Poland",
        "uci_points_total": 2_000
    }
]

race_data: list = [
    {
        "stage_time": "5:00",
        "position": 3,
    }
]


class TestDefaultApiUsage(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='test')
        self.client.login(username='test_user', password='test')
        self.event1: Events = Events.objects.create(**events_data[0])

    def tearDown(self) -> None:
        Events.objects.all().delete()
        Tracks.objects.all().delete()
        Teams.objects.all().delete()
        Riders.objects.all().delete()
        RaceData.objects.all().delete()

    def test_event_list_view(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_get(self):
        url = reverse('event-list')
        data = events_data[0]
        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Events.objects.get().event_title, 'TestEvent1')

    def test_event_post(self):
        url = reverse('event-list')
        data = events_data[1]
        data["tracks"] = list()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Events.objects.filter(event_title='TestEvent2').get().event_title, 'TestEvent2')

    def test_event_patch_method(self):
        url = reverse('event-list')
        events_data[2]['tracks'] = list()
        new_data = {
            "event_title": "test_event_patch_request",
            "event_type": "XC",
            "location": "POL",
            "is_uci_regulated": False,
            "start_date": "2022-02-14",
            "end_date": "2022-02-14",
            "number_of_riders": 17,
            "stages": 0,
            "difficulty": "SR",
            "event_weight": 1.5,
        }

        response_post = self.client.post(url, data=events_data[2])
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        obj = Events.objects.get(event_title=events_data[2]['event_title'])
        url = reverse('event-detail', args=(obj.pk,))

        response_patch = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertNotEqual(events_data[2]["event_title"], new_data["event_title"])

    def test_event_put_method(self):
        url = reverse('event-list')
        events_data[2]['tracks'] = list()
        new_data = {
            "event_title": "test_event_put_request",
            "event_type": "CX",
            "location": "ENG",
            "is_uci_regulated": False,
            "start_date": "2022-02-14",
            "end_date": "2022-02-14",
            "number_of_riders": 20,
            "stages": 1,
            "difficulty": "JR",
            "event_weight": 2.2,
        }

        response_post = self.client.post(url, data=events_data[2])
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        obj = Events.objects.get(event_title=events_data[2]['event_title'])
        url = reverse('event-detail', args=(obj.pk,))

        response_patch = self.client.patch(url, data=new_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertNotEqual(events_data[2]["event_title"], new_data["event_title"])

    def test_event_delete(self):
        get_pk = Events.objects.get(event_title=events_data[0]['event_title']).pk
        url = reverse('event-detail', args=(get_pk,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

