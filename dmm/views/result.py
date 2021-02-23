from .default_imports import *
from ..models import Tag, Specie, Result, Expert, Comment, CommentRound
from django.forms import inlineformset_factory
from ..forms import ResultForm, CommentForm
from django.http import HttpResponseRedirect
from ..helpers import tag_is_present, specie_is_present, tonal_type_is_present

from datetime import datetime

import logging
logger = logging.getLogger(__name__)


class InsertResultView(View):
    def post(self, request):
        if request.is_ajax():
            text = request.POST.get('text')
            title = request.POST.get('title')
            url = request.POST.get('url')
            language_type_id = request.POST.get('language_type_id')
            resource_type_id = request.POST.get('resource_type_id')
            content_type_id = request.POST.get('content_type_id')
            result_date = pytz.utc.localize(dt.strptime(
                request.POST.get('result_date'), '%Y-%m-%dT%H:%M'))
            create_date = timezone.now()
            expert_id = request.POST.get('expert_id')
            logger.info(request.user.expert.name +
                        ' tries to insert result ' + url)
            result = Result(
                text=text,
                title=title,
                url=url,
                language_type_id=language_type_id,
                resource_type_id=resource_type_id,
                content_type_id=content_type_id,
                date=result_date,
                create_date=create_date,
                expert_id=expert_id,
            )
            result.save()
            logger.info(request.user.expert.name +
                        ' successfully inserted result for ' + url)

            return JsonResponse({'result_id': result.id}, status=200)
        return render(request, 'dmm/statistics.html')


def createResult(request):
    logger.debug(request)
    CommentFormSet = inlineformset_factory(Result, Comment, form=CommentForm, can_delete=False, extra=3, max_num=500, min_num=1)

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
                    comm.save()
                else:
                    logger.debug(sub_form.errors)
                    break
            return redirect('')
        else:
            logger.debug(form.errors)
    else:
        form = ResultForm(initial={'expert': request.user.expert})
        formset = CommentFormSet()

    # logger.debug(formset)

    return render(request, 'dmm/result/result_form.html', {'form': form, 'formset': formset})
