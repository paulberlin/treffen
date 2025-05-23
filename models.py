from django.db import models
from django.db.models import Min
from django.db.models import Max
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import date

class User(AbstractUser):
  pass

class Category(models.Model):
  class CategoryType(models.IntegerChoices):
    BUDDY = 1
    LOCATION = 2
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  category_type = models.IntegerField(choices=CategoryType, default=1)

  # Metadata
  class Meta:
    ordering = ['-name']
    unique_together = ('owner', 'name')

  # Methods
  def get_absolute_url(self):
    """Returns the URL to access a particular instance of MyModelName."""
    return reverse('model-detail-view', args=[str(self.id)])

  def __str__(self):
    """String for representing the object (in Admin site etc.)."""
    return self.name

  @property
  def how_often_location(self):
    return Location.objects.filter(category__exact=self.id).count()

  @property
  def how_often_buddy(self):
    return Buddy.objects.filter(category__exact=self.id).count()


class Location(models.Model):
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  lng = models.FloatField(blank=True, null=True)
  lat = models.FloatField(blank=True, null=True)
  category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

  # Metadata
  class Meta:
    ordering = ['-name']
    unique_together = ('owner', 'name')

  # Methods
  def get_absolute_url(self):
    """Returns the URL to access a particular instance of MyModelName."""
    return reverse('model-detail-view', args=[str(self.id)])

  def __str__(self):
    """String for representing the object (in Admin site etc.)."""
    return self.name

  @property
  def how_often(self):
    return Meetup.objects.filter(location__exact=self.id).count()

  @property
  def meetups(self):
    return Meetup.objects.filter(location__exact=self.id).order_by('-date')

  @property
  def date_diff(self):
    min = Meetup.objects.filter(location__exact=self.id).aggregate(Min('date'))
    max = Meetup.objects.filter(location__exact=self.id).aggregate(Max('date'))
    return (max['date__max'] - min['date__min']).days + 1

  @property
  def frequency(self):
    how_often = self.how_often
    if how_often > 0:
      return self.date_diff / how_often
    return 0

  @property
  def latest_meetup(self):
    return Meetup.objects.filter(location__exact=self.id).order_by('-date')[0]


class Buddy(models.Model):
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

  # Metadata
  class Meta:
    ordering = ['name']
    unique_together = ('owner', 'name')

  # Methods
  def get_absolute_url(self):
    """Returns the URL to access a particular instance of MyModelName."""
    return reverse('model-detail-view', args=[str(self.id)])

  def __str__(self):
    """String for representing the object (in Admin site etc.)."""
    return self.name

  @property
  def how_often(self):
    return Meetup.objects.filter(buddies__id__exact=self.id).count()

  @property
  def meetups(self):
    return Meetup.objects.filter(buddies__id__exact=self.id).order_by('-date')

  @property
  def date_diff(self):
    min = Meetup.objects.filter(buddies__id__exact=self.id).aggregate(Min('date'))
    max = Meetup.objects.filter(buddies__id__exact=self.id).aggregate(Max('date'))
    return (max['date__max'] - min['date__min']).days + 1

  @property
  def frequency(self):
    how_often = self.how_often
    if how_often > 0:
      return self.date_diff / how_often
    return 0

  @property
  def latest_meetup(self):
    return Meetup.objects.filter(buddies__id__exact=self.id).order_by('-date')[0]


class Meetup(models.Model):
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  location = models.ForeignKey(Location, on_delete=models.PROTECT)
  buddies = models.ManyToManyField(Buddy)
  date  = models.DateField(default=date.today())

  # check date validity during save
  def save(self, *args, **kwargs):
    if self.date > date.today():
      raise ValidationError("The date cannot be in the future!")
    super(Meetup, self).save(*args, **kwargs)


  # Metadata
  class Meta:
    ordering = ['-name']
    unique_together = ('owner', 'name', 'date', 'location')

  # Methods
  def get_absolute_url(self):
    """Returns the URL to access a particular instance of MyModelName."""
    return reverse('model-detail-view', args=[str(self.id)])

  def __str__(self):
    """String for representing the object (in Admin site etc.)."""
    return self.name
    
  @property
  def buddies_list(self):
    return ", ".join([i.name for i in self.buddies.all()])


class Logger(models.Model):
  page = models.CharField(max_length=250)
  referrer = models.CharField(max_length=250, blank=True, null=True)
  method = models.CharField(max_length=50, blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  # Metadata
  class Meta:
    ordering = ['-timestamp']

  def __str__(self):
    """String for representing the object (in Admin site etc.)."""
    return self.page + " <- " + str(self.referrer)
    
