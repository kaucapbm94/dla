from django.forms import modelformset_factory
from django import forms
from django.forms import formset_factory
from ..models import Book


class BookForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )


BookFormset = formset_factory(BookForm, extra=1)


BookModelFormset = modelformset_factory(
    Book,
    fields=('name', ),
    extra=1,
    widgets={'name': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Book Name here'
    })
    }
)
