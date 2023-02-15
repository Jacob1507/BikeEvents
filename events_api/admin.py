from django.contrib import admin

from .models import Events
from .models import Tracks
from .models import Teams
from .models import Riders
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints


admin.site.register(Events)
admin.site.register(Tracks)
admin.site.register(Teams)
admin.site.register(Riders)
admin.site.register(RaceData)
admin.site.register(EventWeatherConditions)
admin.site.register(EventGeospatialData)
admin.site.register(UciPoints)
