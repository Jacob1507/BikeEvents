from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Event
from .models import Track
from .models import Team
from .models import Rider
from .models import EventParticipant
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
        model = Track
        fields = (
            'event', 'track_name', 'stage_number', 'track_length_meters',
        )


class EventsSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_title', 'event_type', 'location', 'is_uci_regulated',
            'start_date', 'end_date', 'stages',
            'difficulty', 'event_weight', 'tracks', 'participants',
        ]


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('team_name', )


class RidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = (
            'first_name', 'last_name', 'age', 'country', 'team', 'uci_points_total',
        )


class EventParticipantSerializer(serializers.ModelSerializer):
    person = serializers.StringRelatedField()
    event = serializers.StringRelatedField()

    class Meta:
        model = EventParticipant
        fields = '__all__'


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
