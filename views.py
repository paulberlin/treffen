from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.conf import settings
from django.db.models import Count
from datetime import date
from django.db.models.functions import Lower

from .models import Buddy
from .models import Location
from .models import Meetup
from .models import Category

from .forms import AddBuddy
from .forms import AddLocation
from .forms import AddMeetup
from .forms import AddCategory
from .forms import SelectCategory

MAP_LAT = "52.520008"
MAP_LNG = "13.404954"

def index(request):
  context = {}
  if request.user.is_authenticated:
    meetups = Meetup.objects.filter(owner__exact=request.user).order_by('-date')
    latest_meetup = None
    frequency = 0
    days_since_last_meetup = 0
    if meetups:
      latest_meetup = meetups.first()
      first_meetup = meetups.last()
      days_diff = (latest_meetup.date - first_meetup.date).days + 1
      frequency = days_diff / meetups.count()
      days_since_last_meetup = (date.today() - latest_meetup.date).days
    locations = Location.objects.filter(owner__exact=request.user)
    location = None
    location_counter = 0
    for l in locations:
      if l.how_often > location_counter: # we can't sort by property :-/
        location_counter = l.how_often
        location = l
    buddies = Buddy.objects.filter(owner__exact=request.user)
    buddy = None
    buddy_counter = 0
    for b in buddies:
      if b.how_often > buddy_counter: # we can't sort by property :-/
        buddy_counter = b.how_often
        buddy = b
    context = { "meetup": latest_meetup, "location": location, "buddy": buddy, "frequency": frequency, "days_since_last_meetup": days_since_last_meetup }
  return render(request, 'index.html', context)

def about(request):
  context = {}
  return render(request, 'about.html', context)

def logout(request):
  context = {}
  return render(request, 'logout.html', context)

def buddies(request, cat=""):
  if request.user.is_authenticated:
    newbuddy = Buddy(owner=request.user)
    form = AddBuddy(request.user.id, instance=newbuddy)
    open_details = ""
    if request.method == 'POST':
      form = AddBuddy(request.user.id, request.POST, instance=newbuddy)
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('buddies')
      open_details = "open" # show errormessage
    buddies = Buddy.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    category = Category.objects.filter(owner__exact=request.user).filter(name=cat).first()
    category_form = SelectCategory(request.user.id)
    cat_not_found = 0
    if category:
      category_form = SelectCategory(request.user.id, initial={'categories': category.id})
      buddies = Buddy.objects.filter(owner__exact=request.user).filter(category__exact=category).order_by(Lower('name'))
    else:
      cat_not_found = 1
    buddies_without_category = Buddy.objects.filter(owner__exact=request.user).filter(category__isnull=True)
    categories = Category.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'buddies': buddies, "buddies_without_category": buddies_without_category, "form": form, "open_details": open_details, "category_form": category_form, "cat_not_found": cat_not_found, "highlight": "buddies", "categories": categories, "filter": cat }
    return render(request, 'buddies.html', context)
  else:
    return redirect('login')

def buddy_details(request, id):
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    buddy = get_object_or_404(Buddy, pk=id, owner=request.user)
    buddyinstance = get_object_or_404(Buddy, pk=id, owner=request.user)
    form = AddBuddy(request.user.id, instance=buddyinstance)
    if request.method == 'POST':
      form = AddBuddy(request.user.id, request.POST, instance=buddyinstance)
      if request.POST.get('delete') == "1":
        buddyinstance.delete()
        return redirect('buddies')
      if form.is_valid():
	# when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('buddies')
      # validation failed, open form to show error
      open_details = "open"
    last_meetup = Meetup.objects.filter(owner__exact=request.user).filter(buddies=id).order_by('-date').first()
    days_since_last_meetup = 0
    if last_meetup:
      days_since_last_meetup = (date.today() - last_meetup.date).days
    context = { 'buddy': buddy, "form": form, "open_details": open_details, "highlight": "buddies", "last_meetup_days": days_since_last_meetup }
    return render(request, 'buddy.html', context)
  else:
    return redirect('login')


def locations(request):
  if request.user.is_authenticated:
    category_form = SelectCategory(request.user.id)
    newlocation = Location(owner=request.user)
    form = AddLocation(instance=newlocation)
    open_details = ""
    if request.method == 'POST':
      form = AddLocation(request.POST, instance=newlocation)
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('locations')
      open_details = "open"
    locations = Location.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'locations': locations, "form": form, "open_details": open_details, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "category_form": category_form, "highlight": "locations" }
    return render(request, 'locations.html', context)
  else:
    return redirect('login')

def location_details(request, id):
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    location = get_object_or_404(Location, pk=id, owner=request.user)
    locationinstance = get_object_or_404(Location, pk=id, owner=request.user)
    form = AddLocation(instance=locationinstance)
    if request.method == 'POST':
      form = AddLocation(request.POST, instance=locationinstance)
      if request.POST.get('delete') == "1":
        locationinstance.delete()
        return redirect('locations')
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('locations')
      open_details = "open"
    # default 
    map_lng = MAP_LNG
    map_lat = MAP_LAT
    # override with location details if available
    if location.lng:
      map_lng = location.lng
      map_lat = location.lat
    context = { 'location': location, "form": form, "open_details": open_details, "map_lat": map_lat, "map_lng": map_lng, "highlight": "locations" }
    return render(request, 'location.html', context)
  else:
    return redirect('login')


def meetups(request, cat=""):
  if request.user.is_authenticated:
    newmeetup = Meetup(owner=request.user)
    form = AddMeetup(request.user.id, instance=newmeetup)
    open_details = ""
    if request.method == 'POST':
      form = AddMeetup(request.user.id, request.POST, instance=newmeetup)
      if form.is_valid():
	# when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('meetups')
      open_details = "open"
    meetups = Meetup.objects.filter(owner__exact=request.user).order_by('-date')
    category = Category.objects.filter(owner__exact=request.user).filter(name=cat).first()
    category_form = SelectCategory(request.user.id)
    cat_not_found = 0
    if category:
      category_form = SelectCategory(request.user.id, initial={'categories': category.id})
      meetups = Meetup.objects.filter(owner__exact=request.user).filter(category__exact=category).order_by('-date')
    else:
      cat_not_found = 1
    locations_amount = Location.objects.filter(owner__exact=request.user).count()
    buddies_amount = Buddy.objects.filter(owner__exact=request.user).count()
    meetups_amount = meetups.count()
    categories = Category.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'meetups': meetups, "form": form, "locations_amount": locations_amount, "buddies_amount": buddies_amount, "open_details": open_details, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "category_form": category_form, "cat_not_found": cat_not_found, "meetups_amount": meetups_amount, "highlight": "meetups", "categories": categories }
    return render(request, 'meetups.html', context)
  else:
    return redirect('login')


def meetup_details(request, id):
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    meetup = get_object_or_404(Meetup, pk=id, owner=request.user)
    meetupinstance = get_object_or_404(Meetup, pk=id, owner=request.user)
    form = AddMeetup(request.user.id, instance=meetupinstance)
    if request.method == 'POST':
      form = AddMeetup(request.user.id, request.POST, instance=meetupinstance)
      if request.POST.get('delete') == "1":
        meetupinstance.delete()
        return redirect('meetups')
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('meetups')
      open_details = "open"
    context = { 'meetup': meetup, "form": form, "open_details": open_details, "highlight": "meetups" }
    return render(request, 'meetup.html', context)
  else:
    return redirect('login')


def categories(request):
  if request.user.is_authenticated:
    newcategory = Category(owner=request.user)
    form = AddCategory(instance=newcategory)
    open_details = ""
    if request.method == 'POST':
      form = AddCategory(request.POST, instance=newcategory)
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('categories')
      open_details = "open"
    categories = Category.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'categories': categories, "form": form, "open_details": open_details, "highlight": "categories" }
    return render(request, 'categories.html', context)
  else:
    return redirect('login')

def category_details(request, id):
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    category = get_object_or_404(Category, pk=id, owner=request.user)
    categoryinstance = get_object_or_404(Category, pk=id, owner=request.user)
    form = AddCategory(instance=categoryinstance)
    if request.method == 'POST':
      form = AddCategory(request.POST, instance=categoryinstance)
      if request.POST.get('delete') == "1":
        categoryinstance.delete()
        return redirect('categories')
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('categories')
      open_details = "open"
    context = { 'category': category, "form": form, "open_details": open_details, "highlight": "categories" }
    return render(request, 'category.html', context)
  else:
    return redirect('login')

    


