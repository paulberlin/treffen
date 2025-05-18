from django import forms
from django.db.models import Q
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from simplemathcaptcha.fields import MathCaptchaField


from .models import User
from .models import Buddy
from .models import Location
from .models import Meetup
from .models import Category

class SignupForm(UserCreationForm):
  email = forms.EmailField(max_length=200, help_text='Required')
  captcha = MathCaptchaField()

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')


class SelectLocationCategory(forms.Form):
  loc_categories = forms.ModelChoiceField(queryset=Category.objects.all())
  def __init__(self, user, *args, **kwargs):
    super(SelectLocationCategory, self).__init__(*args, **kwargs)
    self.fields['loc_categories'].queryset = Category.objects.filter(owner=user).filter(category_type=2).order_by('name')
    self.fields['loc_categories'].label = "Select a location category to filter"


class SelectBuddyCategory(forms.Form):
  bud_categories = forms.ModelChoiceField(queryset=Category.objects.all())
  def __init__(self, user, *args, **kwargs):
    super(SelectBuddyCategory, self).__init__(*args, **kwargs)
    self.fields['bud_categories'].queryset = Category.objects.filter(owner=user).filter(category_type=1).order_by('name')
    self.fields['bud_categories'].label = "Select a buddy category to filter"


class AddCategory(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

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
    return cleanup(data)

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
    self.fields['category'].queryset = Category.objects.filter(owner=user).filter(category_type=1).order_by('name')

class AddLocation(forms.ModelForm):
  delete = forms.CharField(label='Delete', max_length=1, required=False)
  delete.widget = delete.hidden_widget()
  
  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

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

  def __init__(self, user, *args, **kwargs):
    super(AddLocation, self).__init__(*args, **kwargs)
    self.fields['category'].queryset = Category.objects.filter(owner=user).filter(category_type=2).order_by('name')

class AddMeetup(forms.ModelForm):
  #date = forms.DateField(initial=date.today())
  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

  class Meta:
    model = Meetup
    fields = ('__all__')
    labels = {
      "name": "The happening's name",
      "category": "Category (optional)",
    }
    widgets = {
      "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
      #"date": forms.SelectDateWidget(),
      "owner": forms.HiddenInput(),
    }

  def __init__(self, user, *args, **kwargs):
    super(AddMeetup, self).__init__(*args, **kwargs)
    self.fields['buddies'].queryset = Buddy.objects.filter(owner=user).order_by('name')
    self.fields['location'].queryset = Location.objects.filter(owner=user).order_by('name')
  
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
  

def cleanup(str):
  return str.replace('"', '').replace("'", "`").replace('<', '').replace('>', '')
