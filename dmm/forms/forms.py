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
