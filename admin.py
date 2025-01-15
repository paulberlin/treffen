from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Location
from .models import Buddy
from .models import Meetup
from .models import User

class BuddyAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'how_often')

class LocationAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'how_often')

admin.site.register(Buddy, BuddyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Meetup)
admin.site.register(User, UserAdmin)
