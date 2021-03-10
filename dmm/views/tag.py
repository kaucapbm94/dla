from django.http import HttpResponse
from ..models import Tag, Expert, Result, Comment
from ..helpers.tag import *
from django.views.generic import View
from django.http import HttpResponseRedirect
from ..helpers import get_nrrc
from django import forms
from django.shortcuts import render, redirect
from ..forms import TagForm
import logging
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
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


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def TagCommentRoundsShow(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    results = Result.objects.all()
    result_set = []
    for result in results:
        cms = Comment.objects.filter(result=result)
        for comment in cms:
            if len(comment.commenttags_set.filter(tag=tag)) > 0:
                result_set.append(result)
                break

    nrrc = get_nrrc(result_set, None)

    context = {
        'filter_tag': tag,
        'nrrc': nrrc
    }

    logger.debug(nrrc)
    return render(request, "dmm/result/show.html", context)
