from django.http import HttpResponse
from ..models import Tag, Expert, Result, Comment, TonalType
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


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def TonalTypeCommentRoundsShow(request, tonal_type_id):
    tonal_type = TonalType.objects.get(id=tonal_type_id)
    results = Result.objects.all()
    result_set = []
    for result in results:
        cms = Comment.objects.filter(result=result)
        for comment in cms:
            if comment.tonal_type == tonal_type:
                result_set.append(result)
                break

    nrrc = get_nrrc(result_set, None)

    context = {
        'filter_tonal_type': tonal_type,
        'nrrc': nrrc
    }

    logger.debug(nrrc)
    return render(request, "dmm/result/show.html", context)
