from django.db import models


class Locations(models.Model):
    country = models.CharField(max_length=50)


class Events(models.Model):
    EVENT_TYPES = (
        ('XC', 'cross-country'),
        ('DH', 'downhill'),
        ('CX', 'cyclo-cross'),
        ('FR', 'freeride'),
        ('DJ', 'dirt-jump'),
        ('MX', 'marathon')
    )

    event_title = models.CharField(max_length=50)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=15)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    is_uci_regulated = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_riders = models.IntegerField()
    stages = models.IntegerField()
    difficulty = models.IntegerField()
    event_weight = models.DecimalField(decimal_places=2, max_digits=100)


class Tracks(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    track_name = models.CharField(max_length=50)
    stage_number = models.IntegerField()
    track_length_meters = models.IntegerField()


class Teams(models.Model):
    team_name = models.CharField(max_length=100)


class Riders(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    country = models.ForeignKey(Locations, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    uci_points_total = models.DecimalField(decimal_places=2, max_digits=20_000)


class RaceData(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    rider = models.ForeignKey(Riders, on_delete=models.CASCADE)
    stage_time = models.TimeField()
    position = models.IntegerField()
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)


class EventWeatherConditions(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    weather = models.TextField(max_length=50)
    avg_temp = models.FloatField(max_length=200)
    avg_wind_speed = models.FloatField(max_length=200)


class EventGeospatialData(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()


class UciPoints(models.Model):
    rider_position = models.IntegerField()
    points = models.IntegerField()
