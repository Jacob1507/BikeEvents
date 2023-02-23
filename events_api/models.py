from django.db import models


COUNTRIES = [
    ('POL', 'Poland'),
    ('ENG', 'England'),
    ('USA', 'United States of America'),
    ('CAN', 'Canada'),
    ('NOR', 'Norway'),
    ('NZL', 'New Zealand'),
    ('DEU', 'Germany'),
    ('FRA', 'France'),
]


class Event(models.Model):
    EVENT_TYPES = (
        ('XC', 'cross-country'),
        ('DH', 'downhill'),
        ('CX', 'cyclo-cross'),
        ('FR', 'freeride'),
        ('DJ', 'dirt-jump'),
        ('MX', 'marathon')
    )

    DIFFICULTY = (
        ('JR', 'Juniors'),
        ('AM', 'Amateurs'),
        ('SR', 'Seniors')
    )

    event_title = models.CharField(max_length=50)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=15)
    location = models.CharField(choices=COUNTRIES, max_length=3)
    is_uci_regulated = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    stages = models.IntegerField()
    difficulty = models.CharField(choices=DIFFICULTY, max_length=30)
    event_weight = models.DecimalField(decimal_places=1, max_digits=100)

    def __str__(self):
        return f'{self.event_title} ({self.event_type})'


class Track(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tracks')
    track_name = models.CharField(max_length=50)
    stage_number = models.IntegerField()
    track_length_meters = models.IntegerField()

    class Meta:
        ordering = ['stage_number']

    def __str__(self):
        return f'{self.track_name} (stage: {self.stage_number})'

    def to_dict(self):
        data = {
            "event": self.event.pk,
            "track_name": self.track_name,
            "stage_number": self.stage_number,
            "track_length_meters": self.track_length_meters
        }
        return data


class Team(models.Model):
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


class Rider(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    country = models.CharField(choices=COUNTRIES, max_length=3)
    uci_points_total = models.DecimalField(decimal_places=1, max_digits=20_000, default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EventParticipant(models.Model):
    person = models.ForeignKey(Rider, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'


class RaceData(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    stage_time = models.TimeField()
    position = models.IntegerField()

    def __str__(self):
        return f'{self.event}|{self.track} - {self.rider}'


class EventWeatherConditions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    weather = models.TextField(max_length=50)
    avg_temp = models.FloatField(max_length=200)
    avg_wind_speed = models.FloatField(max_length=200)

    def __str__(self):
        return f'{self.event} - {self.weather}'


class EventGeospatialData(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()


class UciPoints(models.Model):
    rider_position = models.IntegerField()
    points = models.IntegerField()
