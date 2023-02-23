from django.contrib.auth.models import User

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Event
from .models import Track
from .models import Team
from .models import Rider
from .models import EventParticipant
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints

from .serializers import UserSerializer
from .serializers import EventsSerializer
from .serializers import TracksSerializer
from .serializers import TeamsSerializer
from .serializers import RidersSerializer
from .serializers import EventParticipantSerializer
from .serializers import RaceDataSerializer
from .serializers import EventWeatherConditionsSerializer
from .serializers import EventGeospatialDataSerializer
from .serializers import UciPointsSerializer

"""
API endpoints that allows users to be viewed or edited.
"""

# TODO: Implement all CRUDE methods


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=format),
            'events': reverse('event-list', request=request, format=format),
            'tracks': reverse('track-list', request=request, format=format),
            'teams': reverse('team-list', request=request, format=format),
            'riders': reverse('rider-list', request=request, format=format),
            'event_participants': reverse('event-participants-list', request=request, format=format),
            'race_data': reverse('race-data-list', request=request, format=format),
            'event_weather_conditions': reverse('event-weather-conditions-list', request=request, format=format),
            'event_geospatial_data': reverse('event-geospatial-data-list', request=request, format=format),
            'uci_points': reverse('uci-points-list', request=request, format=format)
        }
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event_title = data["event_title"]
        obj.event_type = data["event_type"]
        obj.location = data["location"]
        obj.is_uci_regulated = data["is_uci_regulated"]
        obj.start_date = data["start_date"]
        obj.end_date = data["end_date"]
        obj.stages = data["stages"]
        obj.difficulty = data["difficulty"]
        obj.event_weight = data["event_weight"]

        obj.save()
        serializer = EventsSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event_title = data.get("event_title", obj.event_title)
        obj.event_type = data.get("event_type", obj.event_type)
        obj.location = data.get("location", obj.location)
        obj.is_uci_regulated = data.get("is_uci_regulated", obj.is_uci_regulated)
        obj.start_date = data.get("start_date", obj.start_date)
        obj.end_date = data.get("end_date", obj.end_date)
        obj.stages = data.get("stages", obj.stages)
        obj.difficulty = data.get("difficulty", obj.difficulty)
        obj.event_weight = data.get("event_weight", obj.event_weight)

        obj.save()
        serializer = EventsSerializer(obj)
        return Response(serializer.data)


class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all().order_by('-event__start_date')
    serializer_class = TracksSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TracksSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.track_name = data["track_name"]
        obj.stage_number = data["stage_number"]
        obj.track_length_meters = data["track_length_meters"]

        obj.save()
        serializer = TracksSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.track_name = data.get("track_name", obj.track_name)
        obj.stage_number = data.get("stage_number", obj.stage_number)
        obj.track_length_meters = data.get("track_length_meters", obj.track_length_meters)

        obj.save()
        serializer = TracksSerializer(obj)
        return Response(serializer.data)


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.team_name = data["team_name"]
        obj.save()
        serializer = TeamsSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.team_name = data.get("team_name", obj.team_name)
        obj.save()
        serializer = TeamsSerializer(obj)
        return Response(serializer.data)


class RiderList(generics.ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RidersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class RiderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RidersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.team = data["team"]
        obj.first_name = data["first_name"]
        obj.last_name = data["last_name"]
        obj.age = data["age"]
        obj.country = data["country"]
        obj.uci_points_total = data["uci_points_total"]

        obj.save()
        serializer = RidersSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.team = data.get("team", obj.team)
        obj.first_name = data.get("first_name", obj.first_name)
        obj.last_name = data.get("last_name", obj.last_name)
        obj.age = data.get("age", obj.age)
        obj.country = data.get("country", obj. country)
        obj.uci_points_total = data.get("uci_points_total", obj.uci_points_total)

        obj.save()
        serializer = RidersSerializer(obj)
        return Response(serializer.data)


class EventParticipantList(generics.ListCreateAPIView):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RaceDataList(generics.ListCreateAPIView):
    queryset = RaceData.objects.all().order_by('-event__start_date')
    serializer_class = RaceDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class RaceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RaceData.objects.all()
    serializer_class = RaceDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event = data["event"]
        obj.rider = data["rider"]
        obj.track = data["track"]
        obj.stage_time = data["stage_time"]
        obj.position = data["position"]

        obj.save()
        serializer = RaceDataSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event = data.get("event", obj.event)
        obj.rider = data.get("rider", obj.rider)
        obj.track = data.get("track", obj.track)
        obj.stage_time = data.get("stage_time", obj.stage_time)
        obj.position = data.get("position", obj.position)

        obj.save()
        serializer = RaceDataSerializer(obj)
        return Response(serializer.data)


class EventWeatherConditionsList(generics.ListCreateAPIView):
    queryset = EventWeatherConditions.objects.all().order_by('-event__start_date')
    serializer_class = EventWeatherConditionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class EventWeatherConditionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventWeatherConditions.objects.all()
    serializer_class = EventWeatherConditionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event = data["event"]
        obj.weather = data["weather"]
        obj.avg_temp = data["avg_temp"]
        obj.avg_wind_speed = data["avg_wind_speed"]

        obj.save()
        serializer = EventWeatherConditionsSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event = data.get("event", obj.event)
        obj.weather = data.get("weather", obj.weather)
        obj.avg_temp = data.get("avg_temp", obj.avg_temp)
        obj.avg_wind_speed = data.get("avg_wind_speed", obj.avg_wind_speed)

        obj.save()
        serializer = EventWeatherConditionsSerializer(obj)
        return Response(serializer.data)


class EventGeospatialDataList(generics.ListCreateAPIView):
    queryset = EventGeospatialData.objects.all().order_by('-event__start_date')
    serializer_class = EventGeospatialDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class EventGeospatialDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventGeospatialData.objects.all()
    serializer_class = EventGeospatialDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.event = data["event"]
        obj.longitude = data["longitude"]
        obj.latitude = data["latitude"]

        obj.save()
        serializer = EventGeospatialDataSerializer(obj)
        return Response(serializer.data)


class UciPointsList(generics.ListCreateAPIView):
    queryset = UciPoints.objects.all().order_by('-rider_position')
    serializer_class = UciPointsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save()


class UciPointsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventGeospatialData.objects.all()
    serializer_class = EventGeospatialDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_destroy(self, instance):
        return instance.delete()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data

        obj.rider_position = data["rider_position"]
        obj.points = data["points"]

        obj.save()
        serializer = UciPointsSerializer(obj)
        return Response(serializer.data)
