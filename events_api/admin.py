from django.contrib import admin

from .models import Event
from .models import Track
from .models import Team
from .models import Rider
from .models import RaceData
from .models import EventWeatherConditions
from .models import EventGeospatialData
from .models import UciPoints


admin.site.register(Event)
admin.site.register(Track)
admin.site.register(Team)
admin.site.register(Rider)
admin.site.register(RaceData)
admin.site.register(EventWeatherConditions)
admin.site.register(EventGeospatialData)
admin.site.register(UciPoints)
