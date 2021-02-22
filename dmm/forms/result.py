from django.forms import ModelForm
from django import forms
from django.utils import timezone, dateparse
from datetime import datetime
import pytz
from ..models import *


class ResultForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
              'class': 'form-control border-primary',
            'cols': 120,
            'rows': 2
        }),
        initial='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-primary',
        }),
        initial='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    )
    url = forms.CharField(
        widget=forms.URLInput(attrs={
            'class': 'form-control border-primary',
        }),
        initial='https://github.com/'
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now().strftime("%Y-%m-%dT%H:%M")
    )
    content_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=ContentType.objects.all(),
        initial={'max_number': '1'}
    )
    language_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=LanguageType.objects.all(),
        initial={'max_number': '1'}
    )
    resource_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=ResourceType.objects.all(),
        initial={'max_number': '1'}
    )

    expert = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Expert.objects.all(),
        initial={'max_number': '1'}
    )

    class Meta:
        model = Result

        fields = ['text', 'title', 'url', 'date', 'content_type', 'expert', 'language_type', 'resource_type']
