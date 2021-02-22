import datetime
from datetime import datetime as dt

import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone

from ..models import *


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateTimeModelForm(forms.Form):
    my_date_field = forms.DateTimeField(widget=DateTimeInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(label='E=Mail')
    category = forms.ChoiceField(
        choices=[('question', 'Question'), ('other', 'Other')])
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)


class ProgrammerForm(ModelForm):

    class Meta:
        model = Programmer
        fields = ['name']
