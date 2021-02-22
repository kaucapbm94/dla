from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..forms import ContactForm


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            print(name, email)

    form = ContactForm()
    return render(request, 'dmm/contact/form.html', {'form': form})
