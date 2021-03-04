from ..models import Specie, Expert
from django.http import HttpResponseRedirect
import logging
from django.views.generic import View
from django import forms
from django.shortcuts import render, redirect
from ..forms import SpecieForm
from django.http import HttpResponse
logger = logging.getLogger(__name__)


def SpecieCreate(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    form = SpecieForm(request.POST or None, initial={'expert': expert})
    form.fields['expert'].widget = forms.HiddenInput()
    if form.is_valid():
        instance = form.save()

        # Change the value of the "#id_author". This is the element id in the form
        resp = (
            '<script>' +
            'opener.closeSpeciePopup(window, "%s", "%s");' % (instance.pk, instance) +
            '</script>'
        )
        return HttpResponse(resp)

    return render(request, "dmm/specie/specie_form.html", {"form": form, })
