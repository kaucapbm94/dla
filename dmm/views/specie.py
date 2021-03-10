from ..models import Specie, Expert, Result, Comment
from django.http import HttpResponseRedirect
import logging
from django.views.generic import View
from django import forms
from django.shortcuts import render, redirect
from ..forms import SpecieForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from ..helpers import get_nrrc
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


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def SpecieCommentRoundsShow(request, specie_id):
    specie = Specie.objects.get(id=specie_id)
    results = Result.objects.all()
    result_set = []
    for result in results:
        cms = Comment.objects.filter(result=result)
        for comment in cms:
            if comment.specie == specie:
                result_set.append(result)
                break

    nrrc = get_nrrc(result_set, None)

    context = {
        'filter_specie': specie,
        'nrrc': nrrc
    }

    logger.debug(nrrc)
    return render(request, "dmm/result/show.html", context)
