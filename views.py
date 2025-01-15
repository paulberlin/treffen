from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.conf import settings
from django.db.models import Count

from .models import Buddy
from .models import Location
from .models import Meetup

from .forms import AddBuddy
from .forms import AddLocation
from .forms import AddMeetup

def index(request):
  context = {}
  return render(request, 'index.html', context)

def about(request):
  context = {}
  return render(request, 'about.html', context)

def buddies(request):
  if request.user.is_authenticated:
    newbuddy = Buddy(owner=request.user)
    form = AddBuddy(instance=newbuddy)
    open_details = ""
    if request.method == 'POST':
      form = AddBuddy(request.POST, instance=newbuddy)
      if form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if form.cleaned_data['owner'] != request.user:
          return redirect('index')
        form.save()
        return redirect('buddies')
      open_details = "open"
    buddies = Buddy.objects.filter(owner__exact=request.user).order_by('name')
    context = { 'buddies': buddies, "form": form, "open_details": open_details }
    return render(request, 'buddies.html', context)
  else:
    return redirect('login')

def buddy_details(request, id):
  if request.user.is_authenticated:
    context = {}
    open_details = ""
    buddy = get_object_or_404(Buddy, pk=id, owner=request.user)
    buddyinstance = get_object_or_404(Buddy, pk=id, owner=request.user)
    form = AddBuddy(instance=buddyinstance)
    if request.method == 'POST':
      form = AddBuddy(request.POST, instance=buddyinstance)
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
    context = { 'buddy': buddy, "form": form, "open_details": open_details }
    return render(request, 'buddy.html', context)
  else:
    return redirect('login')

def locations(request):
  if request.user.is_authenticated:
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
    locations = Location.objects.filter(owner__exact=request.user).order_by('name')
    context = { 'locations': locations, "form": form, "open_details": open_details }
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
    context = { 'location': location, "form": form, "open_details": open_details }
    return render(request, 'location.html', context)
  else:
    return redirect('login')


def meetups(request):
  if request.user.is_authenticated:
    newmeetup = Meetup(owner=request.user)
    form = AddMeetup(request.user.id, instance=newmeetup)
    open_details = ""
    if request.method == 'POST':
      form = AddMeetup(request.user.id, request.POST, instance=newmeetup)
      if form.is_valid():
        form.save()
        return redirect('meetups')
      open_details = "open"
    meetups = Meetup.objects.filter(owner__exact=request.user).order_by('-date')
    locations_amount = Location.objects.filter(owner__exact=request.user).count()
    buddies_amount = Buddy.objects.filter(owner__exact=request.user).count()
    context = { 'meetups': meetups, "form": form, "locations_amount": locations_amount, "buddies_amount": buddies_amount, "open_details": open_details }
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
    context = { 'meetup': meetup, "form": form, "open_details": open_details }
    return render(request, 'meetup.html', context)
  else:
    return redirect('login')




