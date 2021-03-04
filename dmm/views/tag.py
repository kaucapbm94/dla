from django.http import HttpResponse
from ..models import Tag, Expert
from ..helpers.tag import *
from django.views.generic import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from ..forms import TagForm
import logging
logger = logging.getLogger(__name__)


def TagCreate(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    form = TagForm(request.POST or None, initial={'expert': expert, })
    form.fields['expert'].widget = forms.HiddenInput()
    logger.debug(request.POST)
    if form.is_valid():
        instance = form.save()

        # Change the value of the "#id_author". This is the element id in the form
        resp = (
            '<script>' +
            'opener.closeTagPopup(window, "%s", "%s", "%s");' % (instance.pk, f"{instance.description} ({instance.expert.name})", instance) +
            '</script>'
        )
        return HttpResponse(resp)

    return render(request, "dmm/tag/tag_form.html", {"form": form, })
