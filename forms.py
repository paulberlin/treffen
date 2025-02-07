from django import forms
from django.db.models import Q
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from datetime import date

from .models import Buddy
from .models import Location
from .models import Meetup
from .models import Category


class SelectCategory(forms.Form):
  categories = forms.ModelChoiceField(queryset=Category.objects.all())

  def __init__(self, user, *args, **kwargs):
    super(SelectCategory, self).__init__(*args, **kwargs)
    self.fields['categories'].queryset = Category.objects.filter(owner=user).order_by('name')
    self.fields['categories'].label = "Select a category to filter"


class AddCategory(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
  def clean_name(self):
    data = self.cleaned_data['name']
    return data.replace('"', '').replace("'", "`").replace('<', '').replace('>', '').replace('/', '')

  class Meta:
    model = Category
    fields = ('__all__')
    labels = {
      "name": "The category's name",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }


class AddBuddy(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
  def clean_name(self):
    data = self.cleaned_data['name']
    return data.replace('"', '').replace("'", "`").replace('<', '').replace('>', '').replace('/', '')

  class Meta:
    model = Buddy
    fields = ('__all__')
    labels = {
      "name": "The mate's name",
      "category": "Category (optional)",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }

  def __init__(self, user, *args, **kwargs):
    super(AddBuddy, self).__init__(*args, **kwargs)
    self.fields['category'].queryset = Category.objects.filter(owner=user).order_by('name')

class AddLocation(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
  def clean_name(self):
    data = self.cleaned_data['name']
    return data.replace('"', '').replace("'", "`").replace('<', '').replace('>', '').replace('/', '')

  class Meta:
    model = Location
    fields = ('__all__')
    labels = {
      "name": "The place's name",
    }
    widgets = {
      "owner": forms.HiddenInput(),
      "lng": forms.HiddenInput(),
      "lat": forms.HiddenInput(),
    }

  def __init__(self, *args, **kwargs):
    super(AddLocation, self).__init__(*args, **kwargs)

class AddMeetup(forms.ModelForm):
  def clean_name(self):
    data = self.cleaned_data['name']
    return data.replace('"', '').replace("'", "`").replace('<', '').replace('>', '').replace('/', '')

  class Meta:
    model = Meetup
    fields = ('__all__')
    labels = {
      "name": "The happening's name",
      "category": "Category (optional)",
    }
    widgets = {
      "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
      "owner": forms.HiddenInput(),
    }

  def __init__(self, user, *args, **kwargs):
    super(AddMeetup, self).__init__(*args, **kwargs)
    self.fields['buddies'].queryset = Buddy.objects.filter(owner=user).order_by('name')
    self.fields['location'].queryset = Location.objects.filter(owner=user).order_by('name')
    self.fields['category'].queryset = Category.objects.filter(owner=user).order_by('name')
  
  def clean(self):
    cleaned_data = super().clean()
    return cleaned_data
  
  def clean_date(self):
    date = self.cleaned_data['date']
    if date > date.today():
      raise ValidationError("The date cannot be in the future!")
    return date

class EditMeetup(AddMeetup):
  # only in edit, we need the delete flag. For Meetup we need to separate the two actions
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
