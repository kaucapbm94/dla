from ..models import Tag, Specie, Result, Expert, Comment, CommentRound, CommentTags, CommentRoundTags
from django.forms import inlineformset_factory
from ..forms import ResultForm, CommentForm, CommentRoundForm
from django.http import HttpResponseRedirect
from ..helpers import tag_is_present, specie_is_present, tonal_type_is_present, make_decision, get_need_round_results_comments, get_nrrc
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
@ allowed_users(allowed_roles=['expert', 'admin', 'primary-expert'])
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
            'specie': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'tonal_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'tags': forms.CheckboxSelectMultiple(attrs={"class": 'my_class'}),
        },
        labels={
            'specie': 'Класс'
        }
    )

    if request.method == 'POST':
        tags = Tag.objects.all()
        formset = CommentRoundFormset(request.POST)
        if formset.is_valid():
            for sub_form in formset:
                if sub_form.is_valid():
                    comm_round = sub_form.save(commit=False)
                    comm_round_tags = sub_form.cleaned_data['tags']
                    comm_round.save()

                    for tag in tags:
                        if tag in comm_round_tags:
                            comm_round_tag = CommentRoundTags.objects.create(tag=tag, is_present=True, comment_round=comm_round)
                        else:
                            comm_round_tag = CommentRoundTags.objects.create(tag=tag, is_present=False, comment_round=comm_round)
                    make_decision(comm_round.comment)
                else:
                    logger.error(sub_form.errors)
        else:
            logger.error(formset.errors)
        return redirect('home')

    # modelformset_factory(Author, widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})})
    initials = []
    tag_allowed_lists = []
    tag_allowed = []
    specie_allowed_list = []
    tonal_type_allowed_list = []
    for comment in comments:
        spec, ton, TAGS = get_allowed(comment, expert_id)
        initials.append({
            'comment': comment,
            'expert': expert
        })
        tag_allowed_lists.append(TAGS)
        tag_allowed.append(True if True in TAGS else False)
        specie_allowed_list.append(spec)
        tonal_type_allowed_list.append(ton)

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
        'tag_allowed': tag_allowed,
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
                    comm.resource_type = result.resource_type
                    comm.save()
                    comm_round = CommentRound.objects.create(clarification=sub_form.cleaned_data['clarification'], comment=comm, expert=request.user.expert)
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
                    logger.debug(comm.tags.all())
                    logger.debug(chosen_tags)
                    for tag in tags:
                        crt = CommentRoundTags.objects.create(tag=tag, is_present=(True if tag in chosen_tags else False), comment_round=comm_round)
                        ct = comm.commenttags_set.all().filter(tag_id=tag.id).delete()
                    comm_round.save()
                    comm.clarification = None
                    comm.save()
                else:
                    logger.error(sub_form.errors)
                    break
            return redirect('home')
        else:
            logger.error(form.errors)
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


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def ResultShow(request, result_id):
    expert = Expert.objects.get(id=request.user.expert.id)
    result = Result.objects.get(id=result_id)
    nrrc = get_nrrc([result], request.user.expert.id)
    context = {
        'nrrc': nrrc,
        'expert': expert
    }
    return render(request, "dmm/result/show.html", context)
