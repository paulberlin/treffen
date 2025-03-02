from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('confirm_logout', views.logout, name='confirm_logout'),
    # buddies
    path('buddies/', views.buddies, name='buddies'),
    path('buddies', views.buddies, name='buddies'),
    path('buddies/<int:id>', views.buddy_details, name='buddy_details'),
    path('buddies/category/<int:cat>', views.buddies, name='buddies_cat'),
    # locations
    path('locations/', views.locations, name='locations'),
    path('locations', views.locations, name='locations'),
    path('locations/<int:id>', views.location_details, name='location_details'),
    path('locations/<str:map>', views.locations, name='locations_map'),
    # meetups
    path('meetups/', views.meetups, name='meetups'),
    path('meetups', views.meetups, name='meetups'),
    path('meetups/<int:id>', views.meetup_details, name='meetup_details'),
    path('meetups/category/<int:cat>', views.meetups, name='meetups_cat'),
    # categories
    path('categories/', views.categories, name='categories'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:id>', views.category_details, name='category_details'),
    # admin stuff
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
