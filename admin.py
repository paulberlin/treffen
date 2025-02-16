from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Location
from .models import Buddy
from .models import Meetup
from .models import Category
from .models import User
from .models import Logger

class BuddyAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner', 'how_often')

class LocationAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner', 'how_often')

class MeetupAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner')

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner')

class LoggerAdmin(admin.ModelAdmin):
  list_display = ('page', 'referrer', 'method', 'timestamp')

admin.site.register(Buddy, BuddyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Logger, LoggerAdmin)
