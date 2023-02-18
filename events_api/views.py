from django.contrib.auth.models import User

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Events
from .models import Tracks
from .models import Teams
from .models import Riders
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints

from .serializers import UserSerializer
from .serializers import EventsSerializer
from .serializers import TracksSerializer
from .serializers import TeamsSerializer
from .serializers import RidersSerializer
from .serializers import RaceDataSerializer
from .serializers import EventWeatherConditionsSerializer
from .serializers import EventGeospatialDataSerializer
from .serializers import UciPointsSerializer

"""
API endpoints that allows users to be viewed or edited.
"""


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=format),
            'events': reverse('event-list', request=request, format=format),
            'tracks': reverse('track-list', request=request, format=format),
            'teams': reverse('team-list', request=request, format=format),
            'riders': reverse('rider-list', request=request, format=format),
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


class EventsList(generics.ListCreateAPIView):
    queryset = Events.objects.all().order_by('-start_date')
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TracksList(generics.ListCreateAPIView):
    queryset = Tracks.objects.all().order_by('-event__start_date')
    serializer_class = TracksSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TracksSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TeamsList(generics.ListCreateAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RidersList(generics.ListCreateAPIView):
    queryset = Riders.objects.all()
    serializer_class = RidersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RiderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Riders.objects.all()
    serializer_class = RidersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RaceDataList(generics.ListCreateAPIView):
    queryset = RaceData.objects.all().order_by('-event__start_date')
    serializer_class = RaceDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RaceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RaceData.objects.all()
    serializer_class = RaceDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EventWeatherConditionsList(generics.ListCreateAPIView):
    queryset = EventWeatherConditions.objects.all().order_by('-event__start_date')
    serializer_class = EventWeatherConditionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EventWeatherConditionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventWeatherConditions.objects.all()
    serializer_class = EventWeatherConditionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EventGeospatialDataList(generics.ListCreateAPIView):
    queryset = EventGeospatialData.objects.all().order_by('-event__start_date')
    serializer_class = EventGeospatialDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EventGeospatialDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventGeospatialData.objects.all()
    serializer_class = EventGeospatialDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UciPointsList(generics.ListCreateAPIView):
    queryset = UciPoints.objects.all().order_by('-rider_position')
    serializer_class = UciPointsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
