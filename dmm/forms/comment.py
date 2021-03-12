from django.forms import ModelForm
from django import forms
from django.utils import timezone
from datetime import datetime
from ..models import Comment, Expert, LanguageType, ResourceType, Result, Specie, TonalType, Tag


class CommentForm(ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-primary', 'rows': 2, 'required': 'true',
                                     'placeholder': 'Текст комментария (Обязательно к заполнению)'}),
        # initial='Текст комментария'
    )
    author_url = forms.CharField(
        widget=forms.URLInput(attrs={'class': 'form-control',  'placeholder': 'https://...', 'required': 'true'}),
        # initial='https://github.com/'
    )
    is_answer = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        initial=False,
        required=False
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': 'true'}),
        # initial=timezone.now().strftime("%Y-%m-%dT%H:%M")
    )
    clarification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    expert = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Expert.objects.all(),
        initial={'max_number': '1'}
    )
    language_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        queryset=LanguageType.objects.all().order_by('id'),
        initial={'max_number': '1'}
    )
    resource_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        queryset=ResourceType.objects.all().order_by('id'),
        initial={'max_number': '1'}
    )
    result = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Result.objects.all()[:6],
        initial={'max_number': '1'}
    )
    specie = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control select-specie', 'required': 'true'}),
        queryset=Specie.objects.all(),
        initial={'max_number': '1'}
    )
    tonal_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control select-tonal_type', 'required': 'true'}),
        queryset=TonalType.objects.all().order_by('id'),
        initial={'max_number': '1'}
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": 'my_class'}),
        required=False
    )

    class Meta:
        model = Comment
        exclude = ()
        fields = ('text', 'author_url', 'is_answer', 'date', 'clarification', 'expert',
                  'language_type', 'resource_type', 'specie', 'result', 'tags', 'tonal_type')
