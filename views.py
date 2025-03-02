import re
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
from .models import Logger

from .forms import AddBuddy
from .forms import AddLocation
from .forms import AddMeetup
from .forms import EditMeetup
from .forms import AddCategory
from .forms import SelectCategory

MAP_LAT = "52.520008"
MAP_LNG = "13.404954"

def index(request):
  log('index', request)
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
    # TODO: do some performance improvements on these "most active" topics
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
    categories = Category.objects.filter(owner__exact=request.user)
    category = None
    category_counter = 0
    for c in categories:
      if (c.how_often_buddy + c.how_often_meetup) > category_counter:
        category_counter = c.how_often_buddy + c.how_often_meetup
        category = c
    context = { "meetup": latest_meetup, "location": location, "buddy": buddy, "frequency": frequency, "days_since_last_meetup": days_since_last_meetup, "category": category }
  return render(request, 'index.html', context)

def about(request):
  log('about', request)
  context = {}
  return render(request, 'about.html', context)

def logout(request):
  log('logout', request)
  context = {}
  return render(request, 'logout.html', context)

def buddies(request, cat=0):
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
        bud = form.save()
        return redirect('buddy_details', bud.id)
      open_details = "open" # show errormessage
    buddies = Buddy.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    category = Category.objects.filter(owner__exact=request.user).filter(id=cat).first()
    category_form = SelectCategory(request.user.id, 1)
    cat_not_found = 0
    if category:
      log('buddies_by_category', request)
      category_form = SelectCategory(request.user.id, 1, initial={'categories': category.id})
      buddies = Buddy.objects.filter(owner__exact=request.user).filter(category__exact=category).order_by(Lower('name'))
    else:
      log('buddies', request)
      cat_not_found = 1
    buddies_without_category = Buddy.objects.filter(owner__exact=request.user).filter(category__isnull=True)
    categories = Category.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'buddies': buddies, "buddies_without_category": buddies_without_category, "form": form, "open_details": open_details, "category_form": category_form, "cat_not_found": cat_not_found, "highlight": "buddies", "categories": categories, "filter": cat }
    return render(request, 'buddies.html', context)
  else:
    return redirect('login')

def buddy_details(request, id):
  log('buddy_details', request)
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
    # prepare a new meetup for the location
    newmeetup = Meetup(owner=request.user)
    #newmeetup.buddies.add(buddy) cannot add a default value before saving :-/
    newmeetup_form = AddMeetup(request.user.id, instance=newmeetup)
    locations_amount = Location.objects.filter(owner__exact=request.user).count()
    context = { 'buddy': buddy, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "form": form, "open_details": open_details, "highlight": "buddies", "last_meetup_days": days_since_last_meetup, "newmeetup_form": newmeetup_form, "locations_amount": locations_amount, "newmeetup_form": newmeetup_form, "locations_amount": locations_amount }
    return render(request, 'buddy.html', context)
  else:
    return redirect('login')


def locations(request, map=""):
  if request.user.is_authenticated:
    newlocation = Location(owner=request.user)
    form = AddLocation(instance=newlocation)
    open_details = ""
    show_map = ""
    if map == "map":
      show_map = "1"
      log('locations/map', request)
    else:
      log('locations', request)
    if request.method == 'POST':
      form = AddLocation(request.POST, instance=newlocation)
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        loc = form.save()
        return redirect('location_details', loc.pk)
      open_details = "open"
    locations = Location.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'locations': locations, "form": form, "open_details": open_details, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "highlight": "locations", "show_map": show_map }
    return render(request, 'locations.html', context)
  else:
    return redirect('login')

def location_details(request, id):
  log('location_details', request)
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
    # prepare a new meetup for the location
    newmeetup = Meetup(owner=request.user, location=location)
    newmeetup_form = AddMeetup(request.user.id, instance=newmeetup)
    buddies_amount = Buddy.objects.filter(owner__exact=request.user).count()
    context = { 'location': location, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "form": form, "open_details": open_details, "map_lat": map_lat, "map_lng": map_lng, "highlight": "locations", "newmeetup_form": newmeetup_form, "buddies_amount": buddies_amount }
    return render(request, 'location.html', context)
  else:
    return redirect('login')


def meetups(request, cat=0):
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
        mup = form.save()
        return redirect('meetup_details', mup.id)
      open_details = "open"
    meetups = Meetup.objects.filter(owner__exact=request.user).order_by('-date')
    category = Category.objects.filter(owner__exact=request.user).filter(id=cat).first()
    category_form = SelectCategory(request.user.id, 2)
    cat_not_found = 0
    if category:
      log('meetups_by_category', request)
      category_form = SelectCategory(request.user.id, 2, initial={'categories': category.id})
      meetups = Meetup.objects.filter(owner__exact=request.user).filter(category__exact=category).order_by('-date')
    else:
      log('meetups', request)
      cat_not_found = 1
    locations_amount = Location.objects.filter(owner__exact=request.user).count()
    buddies_amount = Buddy.objects.filter(owner__exact=request.user).count()
    categories = Category.objects.filter(owner__exact=request.user).order_by(Lower('name'))
    context = { 'meetups': meetups, "form": form, "locations_amount": locations_amount, "buddies_amount": buddies_amount, "open_details": open_details, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "category_form": category_form, "cat_not_found": cat_not_found, "highlight": "meetups", "categories": categories }
    return render(request, 'meetups.html', context)
  else:
    return redirect('login')


def meetup_details(request, id):
  log('meetup_details', request)
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    meetup = get_object_or_404(Meetup, pk=id, owner=request.user)
    meetupinstance = get_object_or_404(Meetup, pk=id, owner=request.user)
    form = EditMeetup(request.user.id, instance=meetupinstance)
    if request.method == 'POST':
      form = EditMeetup(request.user.id, request.POST, instance=meetupinstance)
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
    context = { 'meetup': meetup, "form": form, "map_lat": MAP_LAT, "map_lng": MAP_LNG, "open_details": open_details, "highlight": "meetups" }
    return render(request, 'meetup.html', context)
  else:
    return redirect('login')


def categories(request):
  log('categories', request)
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
    buddy_categories = Category.objects.filter(owner__exact=request.user).filter(category_type=1).order_by(Lower('name'))
    meetup_categories = Category.objects.filter(owner__exact=request.user).filter(category_type=2).order_by(Lower('name'))
    context = { 'buddy_categories': buddy_categories, "meetup_categories": meetup_categories, "form": form, "open_details": open_details, "highlight": "categories" }
    return render(request, 'categories.html', context)
  else:
    return redirect('login')

def category_details(request, id):
  log('category_details', request)
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

    

def log(page, request):
  ref = request.META.get('HTTP_REFERER')
  if ref:
    ref = ref.replace('https://www.buddy-logger.com/', '')
    ref = ref.replace('https://buddy-logger.com/', '')
    ref = ref.replace('http://www.buddy-logger.com/', '')
    ref = ref.replace('http://buddy-logger.com/', '')
    ref = ref.replace('http://www.buddy-logger.com', '')
    ref = ref.replace('http://buddy-logger.com', '')
    ref = re.sub("meetups\/\d+", "meetup_details", ref)
    ref = re.sub("locations\/\d+", "location_details", ref)
    ref = re.sub("buddies\/\d+", "buddy_details", ref)
    ref = re.sub("categories\/\d+", "category_details", ref)
    ref = re.sub("meetups\/category\/\d+", "meetups_by_category", ref)
    ref = re.sub("buddies\/category\/\d+", "buddies_by_category", ref)
    ref = re.sub("\/$", "", ref) # remove last / 
  log = Logger(page=page, referrer=ref, method=request.method)
  log.save()
