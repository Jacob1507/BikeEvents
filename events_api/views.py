from rest_framework import generics

from .models import Locations
from .models import Events
from .models import Tracks
from .models import Teams
from .models import Riders
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints

from .serializers import LocationsSerializer
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


class LocationList(generics.ListCreateAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer


class EventsList(generics.ListCreateAPIView):
    queryset = Events.objects.all().order_by('-start_date')
    serializer_class = EventsSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class TracksList(generics.ListCreateAPIView):
    queryset = Tracks.objects.all().order_by('-event__start_date')
    serializer_class = TracksSerializer


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TracksSerializer


class TeamsList(generics.ListCreateAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer


class RidersList(generics.ListCreateAPIView):
    queryset = Riders.objects.all()
    serializer_class = RidersSerializer


class RiderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Riders.objects.all()
    serializer_class = RidersSerializer


class RaceDataList(generics.ListCreateAPIView):
    queryset = RaceData.objects.all().order_by('-event__start_date')
    serializer_class = RaceDataSerializer


class RaceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RaceData.objects.all()
    serializer_class = RaceDataSerializer


class EventWeatherConditionsList(generics.ListCreateAPIView):
    queryset = EventWeatherConditions.objects.all().order_by('-event__start_date')
    serializer_class = EventWeatherConditionsSerializer


class EventWeatherConditionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventWeatherConditions.objects.all()
    serializer_class = EventWeatherConditionsSerializer


class EventGeospatialDataList(generics.ListCreateAPIView):
    queryset = EventGeospatialData.objects.all().order_by('-event__start_date')
    serializer_class = EventGeospatialDataSerializer


class EventGeospatialDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventGeospatialData.objects.all()
    serializer_class = EventGeospatialDataSerializer


class UciPointsList(generics.ListCreateAPIView):
    queryset = UciPoints.objects.all().order_by('-rider_position')
    serializer_class = UciPointsSerializer
