from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('confirm_logout', views.logout, name='confirm_logout'),
    path('search', views.search, name='search'),
    # buddies
    path('buddies/category/', views.buddies, name='buddies'),
    path('buddies/category', views.buddies, name='buddies'),
    path('buddies/', views.buddies, name='buddies'),
    path('buddies', views.buddies, name='buddies'),
    path('buddies/<int:id>', views.buddy_details, name='buddy_details'),
    path('buddies/category/<int:cat>', views.buddies, name='buddies_cat'),
    # locations
    path('locations/category/', views.locations, name='locations'),
    path('locations/category', views.locations, name='locations'),
    path('locations/', views.locations, name='locations'),
    path('locations', views.locations, name='locations'),
    path('locations/<int:id>', views.location_details, name='location_details'),
    path('locations/map/', views.locations_map, name='locations_map'),
    path('locations/heatmap/', views.locations_heatmap, name='locations_heatmap'),
    path('locations/category/<int:cat>', views.locations, name='locations_cat'),
    # meetups with cal
    path('meetups_cal/', views.meetups_cal, name='meetups_cal'),
    path('meetups_cal', views.meetups_cal, name='meetups_cal'),
    # meetups
    path('meetups/', views.meetups, name='meetups'),
    path('meetups', views.meetups, name='meetups'),
    path('meetups/<int:id>', views.meetup_details, name='meetup_details'),
    path('meetups/category/0-<int:cat>', views.meetups2, name='meetups_cat2'),
    path('meetups/category/<int:cat>-0', views.meetups3, name='meetups_cat3'),
    path('meetups/category/<str:cat>', views.meetups, name='meetups_cat'),
    # categories
    path('categories/', views.categories, name='categories'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:id>', views.category_details, name='category_details'),
    # admin stuff
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
