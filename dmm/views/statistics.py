
import json
from ..models import *
from ..helpers.user import *
from ..helpers import get_need_round_results_comments
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import CharField, Value
from ..helpers import get_allowed, is_result_marked_up, make_decision, get_nrrc
import logging
logger = logging.getLogger(__name__)


@login_required(login_url='login')
@allowed_users(allowed_roles=['expert'])
def Statistics(request):
    species = Specie.objects.values()
    tags = Tag.objects.values()
    tonal_types = TonalType.objects.values()
    expert_id = request.user.expert.id
    results = Result.objects.all().annotate(number_of_comments=Count('comment')).order_by('-created')

    for specie in species:
        rounds_count = CommentRound.objects.filter(specie_id=specie['id']).count()
        specie['expert_name'] = Expert.objects.get(id=specie['expert_id'])
        comment_count = Comment.objects.filter(specie_id=specie['id']).count()
        specie['rounds_count'] = rounds_count
        specie['comment_count'] = comment_count

    for tag in tags:
        rounds_count = CommentRound.objects.filter(tags__name=tag['name']).count()
        comment_count = Comment.objects.filter(tags__name=tag['name']).count()
        tag['expert_name'] = Expert.objects.get(id=tag['expert_id'])
        tag['rounds_count'] = rounds_count
        tag['comment_count'] = comment_count

    for tonal_type in tonal_types:
        rounds_count = CommentRound.objects.filter(tonal_type_id=tonal_type['id']).count()
        comment_count = Comment.objects.filter(tonal_type_id=tonal_type['id']).count()
        tonal_type['rounds_count'] = rounds_count
        tonal_type['comment_count'] = comment_count

    nrrc = get_nrrc([result for result in results], expert_id)

    experts = Expert.objects.all()
    expert_stats = {}
    for expert in experts:
        expert_stats[expert] = {}
        comment_rounds = CommentRound.objects.filter(expert=expert).order_by('created')
        expert_stats[expert]['comment_rounds'] = comment_rounds
        expert_stats[expert]['last_round_date'] = comment_rounds[0].created if len(comment_rounds) > 0 else None
        expert_stats[expert]['round_count'] = len(comment_rounds)

    context = {
        'tags': tags,
        'tonal_types': tonal_types,
        'species': species,
        'nrrc': nrrc,
        'expert_stats': expert_stats,
    }
    return render(request, 'dmm/comment/statistics.html', context)
