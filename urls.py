from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    # buddies
    path('buddies/', views.buddies, name='buddies'),
    path('buddies', views.buddies, name='buddies'),
    path('buddies/<int:id>', views.buddy_details, name='buddy_details'),
    # locations
    path('locations/', views.locations, name='locations'),
    path('locations', views.locations, name='locations'),
    path('locations/<int:id>', views.location_details, name='location_details'),
    # meetups
    path('meetups/', views.meetups, name='meetups'),
    path('meetups', views.meetups, name='meetups'),
    path('meetups/<int:id>', views.meetup_details, name='meetup_details'),
    # admin stuff
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]