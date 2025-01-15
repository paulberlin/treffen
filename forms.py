from django import forms
from django.db.models import Q
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
import datetime

from .models import Buddy
from .models import Location
from .models import Meetup

class AddBuddy(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  class Meta:
    model = Buddy
    fields = ('__all__')
    #exclude = ['owner']
    labels = {
      "name": "The mate's name",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }

  def __init__(self, *args, **kwargs):
    super(AddBuddy, self).__init__(*args, **kwargs)

class AddLocation(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  class Meta:
    model = Location
    #exclude = ['owner']
    fields = ('__all__')
    labels = {
      "name": "The place's name",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }

  def __init__(self, *args, **kwargs):
    super(AddLocation, self).__init__(*args, **kwargs)

class AddMeetup(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  class Meta:
    model = Meetup
    #exclude = ['owner']
    fields = ('__all__')
    labels = {
      "name": "The happening's name",
    }
    widgets = {
      "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
      "owner": forms.HiddenInput(),
    }

  def __init__(self, user, *args, **kwargs):
    super(AddMeetup, self).__init__(*args, **kwargs)
    self.fields['buddies'].queryset = Buddy.objects.filter(owner=user)
    self.fields['location'].queryset = Location.objects.filter(owner=user)
  
  def clean(self):
    cleaned_data = super().clean()
    return cleaned_data
  
  def clean_date(self):
    date = self.cleaned_data['date']
    if date > datetime.date.today():
      raise ValidationError("The date cannot be in the future!")
    return date





