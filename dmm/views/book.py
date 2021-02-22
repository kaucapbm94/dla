from ..forms import BookModelFormset
from django.shortcuts import render, redirect

from ..forms import BookFormset
from ..models import Book


def create_book_normal(request):
    template_name = 'dmm/create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                if name:
                    Book(name=name).save()

            return redirect('book_list')

    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })


def create_book_model_form(request):
    template_name = 'dmm/create_normal.html'
    heading_message = 'Model Formset Demo'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = BookModelFormset(queryset=Book.objects.all())
    elif request.method == 'POST':
        formset = BookModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get('name'):
                    form.save()
            return redirect('book_list')

    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
