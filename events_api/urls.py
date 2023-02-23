from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from events_api import views


urlpatterns = [
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('tracks/', views.TrackList.as_view(), name='track-list'),
    path('tracks/<int:pk>/', views.TrackDetail.as_view(), name='track-detail'),
    path('teams/', views.TeamList.as_view(), name='team-list'),
    path('teams/<int:pk>/', views.TeamDetail.as_view(), name='team-detail'),
    path('riders/', views.RiderList.as_view(), name='rider-list'),
    path('riders/<int:pk>/', views.RiderDetail.as_view(), name='rider-detail'),
    path('race-data/', views.RaceDataList.as_view(), name='race-data-list'),
    path('race-data/<int:pk>/', views.RaceDataDetail.as_view(), name='race-data-detail'),
    path('event-weather-conditions/', views.EventWeatherConditionsList.as_view(),
         name='event-weather-conditions-list'),
    path('event-weather-conditions/<int:pk>/', views.EventWeatherConditionsDetail.as_view(),
         name='event-weather-conditions-detail'),
    path('event-geospatial-data/', views.EventGeospatialDataList.as_view(),
         name='event-geospatial-data-list'),
    path('event-geospatial-data/<int:pk>/', views.EventGeospatialDataDetail.as_view(),
         name='event-geospatial-data-detail'),
    path('uci-points/', views.UciPointsList.as_view(), name='uci-points-list'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)
