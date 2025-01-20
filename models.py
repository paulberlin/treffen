from django.db import models
from django.db.models import Min
from django.db.models import Max
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import datetime

class User(AbstractUser):
  pass

class Category(models.Model):
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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


class Location(models.Model):
  # Fields
  name = models.CharField(max_length=50)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  lng = models.CharField(max_length=50, blank=True)
  lat = models.CharField(max_length=50, blank=True)

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
  def clean_name(self):
    return self.name.replace("'", "`") # change ' into `

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
  date  = models.DateField()
  category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

  # check date validity during save
  def save(self, *args, **kwargs):
    if self.date > datetime.date.today():
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

  @property
  def clean_name(self):
    return self.name.replace("'", "`") # change ' into `




