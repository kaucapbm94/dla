from .default_imports import *
from ..models import Tag, Specie, Result, Expert, Comment
from django.forms import inlineformset_factory
from ..forms import ResultForm, CommentForm
from django.http import HttpResponseRedirect

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
    CommentFormSet = inlineformset_factory(Result, Comment, form=CommentForm, can_delete=False, extra=3, max_num=1)

    if request.method == 'POST':
        form = ResultForm(request.POST)
        logger.debug(form.is_valid())
        if form.is_valid():
            logger.debug(request.POST.get("round_tags", ""))
            result = form.save()
            formset = CommentFormSet(request.POST, instance=result)
            if formset.is_valid():
                formset.save()
                return redirect('programmer_new')
            else:
                logger.debug(formset.errors)
        else:
            logger.debug(form.errors)

    else:
        form = ResultForm(initial={'expert': request.user.expert})
        formset = CommentFormSet()

    # logger.debug(formset)

    return render(request, 'dmm/result/result_form.html', {'form': form, 'formset': formset})
