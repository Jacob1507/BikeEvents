from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Events
from .models import Tracks
from .models import Teams
from .models import Riders
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = (
            'event', 'track_name', 'stage_number', 'track_length_meters',
        )


class EventsSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Events
        fields = [
            'event_title', 'event_type', 'location', 'is_uci_regulated',
            'start_date', 'end_date', 'number_of_riders', 'stages',
            'difficulty', 'event_weight', 'tracks',
        ]


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('team_name', )


class RidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riders
        fields = (
            'first_name', 'last_name', 'age', 'country', 'team', 'uci_points_total',
        )


class RaceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceData
        fields = (
            'event', 'rider', 'stage_time', 'position', 'track',
        )


class EventWeatherConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWeatherConditions
        fields = (
            'event', 'weather', 'avg_temp', 'avg_wind_speed',
        )


class EventGeospatialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGeospatialData
        fields = (
            'event', 'longitude', 'latitude',
        )


class UciPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UciPoints
        fields = (
            'rider_positions', 'points',
        )
