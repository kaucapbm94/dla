from .default_imports import *
from ..models import *
from ..helpers.user import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['expert'])
def Statistics(request):
    species = Specie.objects.values()
    tags = Tag.objects.values()
    comments = Comment.objects.values()
    groups = request.user.groups.values_list('name', flat=True)
    is_primary = False
    expert_ids = []
    for group in groups:
        if group in super_user_group_names():
            is_primary = True

    if is_primary:
        expert_ids = Expert.objects.values_list('id', flat=True)
    else:
        expert_ids.append(request.user.expert.id)
    comment_rounds = CommentRound.objects.filter(expert_id__in=expert_ids).values(
        'comment_id',
        'comment__text',
        'specie__name',
        'tonal_type__name',
        'expert__name',
        'create_date'
    ).order_by('-create_date')

    for comment_round in comment_rounds:
        my_tags = Tag.objects.filter(commentround__comment_id=comment_round['comment_id'],
                                     commentround__expert__id=request.user.expert.id).values('name')
        tag_names = ''
        for my_tag in my_tags:
            tag_names += my_tag['name'] + ', '
        comment_round['tag_names'] = tag_names

    stats = {'waiting_round1': 0, 'waiting_round2': 0, 'waiting_round3': 0}

    for comment in comments:
        comment_round_count = CommentRound.objects.filter(
            comment_id=comment['id']).count()
        if comment_round_count == 0:
            stats['waiting_round1'] += 1
        elif comment_round_count == 1:
            stats['waiting_round2'] += 1
        elif comment_round_count == 2:
            stats['waiting_round3'] += 1

    for specie in species:
        total_count = CommentRound.objects.filter(
            specie_id=specie['id']).count()
        specie['expert_name'] = Expert.objects.get(id=specie['expert_id'])
        specie['total_count'] = total_count

    for tag in tags:
        total_count = CommentRound.objects.filter(
            tags__name=tag['name']).count()
        tag['expert_name'] = Expert.objects.get(id=tag['expert_id'])
        tag['total_count'] = total_count

    context = {
        'tags': tags,
        'stats': stats,
        'species': species,
        'comment_rounds': comment_rounds,
    }
    return render(request, 'dmm/comment/statistics.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['expert'])
def WaitingRounds(request):

    nrrc = get_need_round_results_comments(request)

    context = {
        'need_round_results_comments': nrrc,
    }
    return render(request, 'dmm/comment/waiting_rounds.html', context)
