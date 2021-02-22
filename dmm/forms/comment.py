from django.forms import ModelForm
from django import forms
from django.utils import timezone
from datetime import datetime
from ..models import *


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return "%s(%s)" % (tag.name, tag.expert.name)


class CommentForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-primary'}),
        initial='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed elementum sem ac magna suscipit, non.')
    author_url = forms.CharField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        initial='https://github.com/'
    )
    is_answer = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        initial=False,
        required=False
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now().strftime("%Y-%m-%dT%H:%M")
    )
    clarification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    )
    expert = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Expert.objects.all(),
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
    result = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Result.objects.all()[:6],
        initial={'max_number': '1'}
    )
    round_tags = CustomMMCF(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Comment
        exclude = ()
        fields = ('text', 'author_url', 'is_answer', 'date', 'clarification', 'expert',
                  'language_type', 'resource_type', 'result')

    def save(self, commit=True):
        instance = super(CommentForm, self).save(commit=False)
        instance.author_url = 'OLOLO'
        if commit:
            instance.save()
        return instance
