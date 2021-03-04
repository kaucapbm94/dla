from ..models import Tag, Specie, Result, Expert, Comment, CommentRound, CommentTags, CommentRoundTags
from django.forms import inlineformset_factory
from ..forms import ResultForm, CommentForm, CommentRoundForm
from django.http import HttpResponseRedirect
from ..helpers import tag_is_present, specie_is_present, tonal_type_is_present
from django.forms import formset_factory, modelformset_factory
from django import forms
from ..helpers import get_allowed
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from datetime import datetime
from django.shortcuts import render, redirect
from django.db.models import Count, F, Value

import logging
logger = logging.getLogger(__name__)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def roundResult(request, result_id):
    result = Result.objects.get(id=result_id)
    expert_id = request.user.expert.id
    comments = Comment.objects.filter(result=result)
    expert = Expert.objects.get(id=request.user.expert.id)
    # CommentRoundFormset = formset_factory(CommentRoundForm, extra=len(comments))
    CommentRoundFormset = modelformset_factory(
        CommentRound,
        # form=CommentRoundForm,
        extra=len(comments),
        fields=['clarification', 'comment', 'expert', 'specie', 'tonal_type', 'tags'],
        widgets={
            'clarification': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.HiddenInput(),
            'expert': forms.HiddenInput(),
            'specie': forms.Select(attrs={'class': 'form-control'}),
            'tonal_type': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={"class": 'my_class'}),
        },
        labels={
            'specie': 'Класс'
        }
    )

    if request.method == 'POST':
        tags = Tag.objects.all()
        logger.debug(request.POST)
        formset = CommentRoundFormset(request.POST)
        logger.debug(formset)
        if formset.is_valid():
            for sub_form in formset:
                if sub_form.is_valid():
                    comm_round = sub_form.save(commit=False)
                    comm_round_tags = sub_form.cleaned_data['tags']
                    comm_round.save()
                    logger.debug(comm_round.__dict__)

                    for tag in tags:
                        if tag in comm_round_tags:
                            comm_round_tag = CommentRoundTags.objects.create(tag=tag, is_present=True, comment_round=comm_round)
                        else:
                            comm_round_tag = CommentRoundTags.objects.create(tag=tag, is_present=False, comment_round=comm_round)

                else:
                    logger.debug(sub_form.errors)
        else:
            logger.debug(formset.errors)
        return redirect('waiting_rounds')

    # modelformset_factory(Author, widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})})
    initials = []
    tag_allowed_lists = []
    specie_allowed_list = []
    tonal_type_allowed_list = []
    for comment in comments:
        spec, ton, TAGS = get_allowed(comment, expert_id)
        initials.append({
            'comment': comment,
            'expert': expert
        })
        tag_allowed_lists.append(TAGS)
        specie_allowed_list.append(True if spec else comment.specie)
        tonal_type_allowed_list.append(True if ton else comment.tonal_type)

    formset = CommentRoundFormset(
        queryset=CommentRound.objects.none(),
        initial=initials
    )

    tags = Tag.objects.all()

    context = {
        'tags': tags,
        'result': result,
        'formset': formset,
        'comments': comments,
        'tag_allowed_lists': tag_allowed_lists,
        'specie_allowed_list': specie_allowed_list,
        'tonal_type_allowed_list': tonal_type_allowed_list,
    }

    return render(request, 'dmm/result/result_round.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def createResult(request):
    CommentFormSet = inlineformset_factory(
        Result,
        Comment,
        form=CommentForm,
        can_delete=False,
        extra=0,
        max_num=500,
        min_num=1,
    )

    if request.method == 'POST':
        form = ResultForm(request.POST)
        logger.debug(request.POST)
        my_dict = request.POST

        if form.is_valid():
            result = form.save()
            formset = CommentFormSet(request.POST, instance=result)

            for sub_form in formset:
                if sub_form.is_valid():
                    chosen_tags = sub_form.cleaned_data['tags']
                    comm = sub_form.save()
                    comm_round = CommentRound.objects.create(clarification=sub_form.cleaned_data['clarification'], comment=comm, expert=request.user.expert)
                    # sub_form.save_m2m()
                    # assign specie if enough votes else round it
                    spec = sub_form.cleaned_data['specie']
                    if specie_is_present(comm, spec):
                        comm.specie = spec
                    else:
                        comm_round.specie = spec
                        comm.specie = None
                        # make decision about tags
                    tonal_type = sub_form.cleaned_data['tonal_type']
                    if tonal_type_is_present(comm, tonal_type):
                        comm.tonal_type = tonal_type
                    else:
                        comm_round.tonal_type = tonal_type
                        comm.tonal_type = None
                        # make decision about tags
                    tags = Tag.objects.all()
                    for tag in tags:
                        # if tag is already in comment_tags for the comment
                        if tag in comm.tags.all():
                            continue
                        # if tag is definitely present/absent/still not defined for the comment
                        is_present = tag_is_present(comm, tag)
                        if is_present is not None:
                            ct = CommentTags.objects.create(tag=tag, comment=comm, is_present=is_present)
                        else:
                            crt = CommentRoundTags.objects.create(tag=tag, is_present=(True if tag in chosen_tags else False), comment_round=comm_round)
                    comm_round.save()
                    comm.clarification = None
                    comm.save()
                else:
                    logger.debug(sub_form.errors)
                    break
            return redirect('waiting_rounds')
        else:
            logger.debug(form.errors)
    else:
        form = ResultForm(initial={'expert': request.user.expert})
        formset = CommentFormSet()

    formset = CommentFormSet()
    tags = Tag.objects.all()
    context = {
        'form': form,
        'formset': formset,
        'tags': tags
    }

    return render(request, 'dmm/result/result_form.html', context)


def ResultShow(request, result_id):
    expert = Expert.objects.get(id=request.user.expert.id)
    result = Result.objects.get(id=result_id)
    comments = Comment.objects.filter(result=result)
    logger.debug('SHOWING')
    logger.debug(comments)
    for comment in comments:
        logger.debug(comment.commenttags_set.all())
    context = {
        'result': result,
        'expert': expert
    }
    return render(request, "dmm/result/show.html", context)
