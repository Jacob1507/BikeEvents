from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from events_api import views


urlpatterns = [
    path('events/', views.EventsList.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
    path('tracks/', views.TracksList.as_view()),
    path('tracks/<int:pk>/', views.TrackDetail.as_view()),
    path('teams/', views.TeamsList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('riders/', views.RidersList.as_view()),
    path('riders/<int:pk>/', views.RiderDetail.as_view()),
    path('race-data/', views.RaceDataList.as_view()),
    path('race-data/<int:pk>/', views.RaceDataDetail.as_view()),
    path('event-weather-conditions/', views.EventWeatherConditionsList.as_view()),
    path('event-weather-conditions/<int:pk>/', views.EventWeatherConditionsDetail.as_view()),
    path('event-geospatial-data/', views.EventGeospatialDataList.as_view()),
    path('event-geospatial-data/<int:pk>/', views.EventGeospatialDataDetail.as_view()),
    path('uci-points/', views.UciPointsList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
