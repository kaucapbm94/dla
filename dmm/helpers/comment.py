from ..models import *
from .default_imports import *


# returns true if 'tag' was considered 2 or more times as is_present=true/false for the 'comment'
def tag_is_present(comment, tag):
    # firstly get all comment_rounds for the comment
    comment_rounds = CommentRound.objects.filter(comment=comment)
    # in the queryset search now any instances of the comment_round_tag containing 'tag' and count is_present
    if CommentRoundTags.objects.filter(comment_round__in=comment_rounds, tag=tag, is_present=True).count() >= 1:
        is_present = True
    elif CommentRoundTags.objects.filter(comment_round__in=comment_rounds, tag=tag, is_present=False).count() >= 1:
        is_present = False
    else:
        is_present = None
    return is_present


def specie_is_present(comment, specie):
    return True if CommentRound.objects.filter(comment=comment, specie=specie).count() >= 1 else False


def tonal_type_is_present(comment, tonal_type):
    return True if CommentRound.objects.filter(comment=comment, tonal_type=tonal_type).count() >= 1 else False


def specie_winner(comment):
    species = Specie.objects.all()
    for spec in species:
        if CommentRound.objects.filter(comment=comment, specie=spec).count() >= 2:
            return spec
    return None


def get_need_round_comments(result, expert_id):
    comments = result.comment_set.all()
    need_round_comments = {}

    # take all properties, which need additional rounds
    for com in comments:
        # get all rounds of the comment
        comment_rounds = CommentRound.objects.filter(comment=com)

        # by default every comment has specie and doesn't need round for it
        specie_needs_round = False
        # skip if current expert has voted for specie for the comment
        if com.specie is None:
            specie_needs_round = True
            # but if there are enough rounds for some specie, assign specie and don't round for it
            comment_species = [cr.specie for cr in comment_rounds]
            comment_specie_rounds_counts = {
                i: comment_species.count(i) for i in comment_species}
            for spec in comment_specie_rounds_counts:
                if comment_specie_rounds_counts[spec] >= 3:
                    com.specie = spec
                    com.save()
                    specie_needs_round = False
                    break
            if expert_id in [cr.expert_id for cr in comment_rounds]:
                specie_needs_round = False

        # by default every comment has tonal_type and doesn't need round for it
        tonal_type_needs_round = False
        if com.tonal_type is None:
            tonal_type_needs_round = True
            # but if there are enough rounds for some tonal_type, assign tonal_type and don't round for it
            comment_tonal_types = [cr.tonal_type for cr in comment_rounds]
            comment_tonal_type_rounds_count = {
                i: comment_tonal_types.count(i) for i in comment_tonal_types}
            for tonal_type in comment_tonal_type_rounds_count:
                if comment_tonal_type_rounds_count[tonal_type] >= 3:
                    com.specie = tonal_type
                    com.save()
                    break
            if expert_id in [cr.expert_id for cr in comment_rounds]:
                tonal_type_needs_round = False

        """ by default every comment hasn't tag_ids to round"""
        comment_rounds_tags = []
        for cr in comment_rounds:
            for cr_tag in CommentRoundTags.objects.filter(comment_round_id=cr.id):
                comment_rounds_tags.append(cr_tag)

        # exclude assigned tags
        rounded_by_expert_tag_ids = [comment_rounds_tag.tag_id for comment_rounds_tag in comment_rounds_tags if
                                     comment_rounds_tag.comment_round.expert_id == expert_id]
        # rounded_by_expert_tag_ids = []
        logger.debug(rounded_by_expert_tag_ids)
        tags = Tag.objects.exclude(id__in=com.tags.values_list('id', flat=True)).exclude(
            id__in=rounded_by_expert_tag_ids)
        tag_stats = {i: (
            [t.tag for t in comment_rounds_tags if t.is_present ==
                True].count(i),
            [t.tag for t in comment_rounds_tags if t.is_present ==
                False].count(i),
            [t.tag for t in comment_rounds_tags if t.is_present is None].count(
                i),
        ) for i in tags}

        # if tag has 3 or more voices then assign it to the comment and exclude from tags
        for TAG in tag_stats:
            for i in range(0, 3):
                if tag_stats[TAG][i] >= 3:
                    CommentTags.objects.create(tag=TAG, comment=com,
                                               is_present=(True if i == 0 else (False if i == 1 else None)))
                    # exclude assigned tags and rounded by the expert tags
                    tags = Tag.objects.exclude(id__in=com.tags.values_list('id', flat=True)).exclude(
                        id__in=rounded_by_expert_tag_ids)
        # remaining tags convert to ids
        tag_ids_need_round = [TAG.id for TAG in tags]

        need_round_comments[com] = {'specie_needs_round': specie_needs_round,
                                    'tag_ids_need_round': tag_ids_need_round,
                                    'tonal_type_needs_round': tonal_type_needs_round}
    return need_round_comments


def get_need_round_results_comments(request):
    species = Specie.objects.values()
    expert_id = request.user.expert.id

    # expert primary? show statistics : nothing
    groups = request.user.groups.values_list('name', flat=True)
    super_users = ['admin', 'primary_expert']
    is_primary = False
    expert_ids = []
    for group in groups:
        if group in super_users:
            is_primary = True
    if is_primary:
        expert_ids = Expert.objects.values_list('id', flat=True)
    else:
        expert_ids.append(expert_id)

    results = Result.objects.all()

    nrrc = {}

    for result in results:
        # logger.debug(get_comments(result.comment_set.all(), expert_id))
        nrrc[result] = get_need_round_comments(result, expert_id)
    logger.debug(nrrc)
    return nrrc
