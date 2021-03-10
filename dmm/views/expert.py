from ..models import Expert, CommentRound, CommentRoundTags, CommentTags, Result, Comment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from ..helpers import get_nrrc
import logging
logger = logging.getLogger(__name__)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def ExpertCommentRoundsShow(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    results = Result.objects.all()
    result_set = []
    for result in results:
        decision = False
        cms = Comment.objects.filter(result=result)
        for comment in cms:
            if len(comment.commentround_set.filter(expert=expert)) > 0:
                result_set.append(result)
                break

    nrrc = get_nrrc(result_set, expert_id)

    context = {
        'filter_expert': expert,
        'nrrc': nrrc
    }

    logger.debug(nrrc)
    return render(request, "dmm/result/show.html", context)
