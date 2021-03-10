from itertools import chain
from ..models import *
from .result import is_result_marked_up


def get_allowed(comment, expert_id):
    comment_rounds = CommentRound.objects.filter(comment=comment)
    # logger.debug(CommentRoundTags.objects.filter(comment_round__in=[]))
    specie_needs_round = False
    # skip if current expert has voted for specie for the comment
    if comment.specie is None:
        specie_needs_round = True
        # but if there are enough rounds for some specie, assign specie and don't round for it
        comment_species = [cr.specie for cr in comment_rounds]
        comment_specie_rounds_counts = {
            i: comment_species.count(i) for i in comment_species}
        for spec in comment_specie_rounds_counts:
            if comment_specie_rounds_counts[spec] >= 3:
                comment.specie = spec
                comment.save()
                specie_needs_round = False
                break
        if expert_id in [cr.expert_id for cr in comment_rounds]:
            specie_needs_round = False

    # by default every comment has tonal_type and doesn't need round for it
    tonal_type_needs_round = False
    if comment.tonal_type is None:
        tonal_type_needs_round = True
        # but if there are enough rounds for some tonal_type, assign tonal_type and don't round for it
        comment_tonal_types = [cr.tonal_type for cr in comment_rounds]
        comment_tonal_type_rounds_count = {
            i: comment_tonal_types.count(i) for i in comment_tonal_types}
        for tonal_type in comment_tonal_type_rounds_count:
            if comment_tonal_type_rounds_count[tonal_type] >= 3:
                comment.tonal_type = tonal_type
                comment.save()
                break
        if expert_id in [cr.expert_id for cr in comment_rounds]:
            tonal_type_needs_round = False

    allowed_tag_list = []
    tags = Tag.objects.all()
    # take all comment rounds of the comment and check
    comment_rounds = CommentRound.objects.filter(comment=comment)
    expert_comment_rounds = comment_rounds.filter(expert_id=expert_id)
    comment_rounds_tags_ids = CommentRoundTags.objects.filter(comment_round__in=expert_comment_rounds).values_list('tag_id', flat=True)
    for tag in tags:
        # purpose: check total round count, check if expert has already rounded this tag for this comment
        if CommentRoundTags.objects.filter(tag=tag, comment_round__in=comment_rounds).count() < 3 and tag.id not in comment_rounds_tags_ids:
            allowed_tag_list.append(True)
        else:
            allowed_tag_list.append(False)

    return specie_needs_round, tonal_type_needs_round, allowed_tag_list


def get_nrrc(results, expert_id):
    # nrrc = {
    #     result: {
    #         'comments': {
    #               comment: {
    #                   'specie_needs_round': bool,
    #                   'tag_ids_need_round': [tag.name, tag.name, tag.name, ...],
    #                   'tonal_type_needs_round': bool,
    #               }
    #         }
    #         'markup_possible': bool,
    #     }
    # }

    nrrc = {}
    for result in results:
        comments = {}
        for comment in result.comment_set.all():
            comments[comment] = get_need_round_results_comments(comment, expert_id)
        nrrc[result] = {}
        nrrc[result]['comments'] = comments
        markup_possible = False
        for comment in nrrc[result]['comments']:
            if nrrc[result]['comments'][comment]['specie_needs_round'] or nrrc[result]['comments'][comment]['tonal_type_needs_round'] or len(nrrc[result]['comments'][comment]['tag_ids_need_round']) > 0:
                markup_possible = True
            # logger.debug(nrrc[result]['comments'][comment]['specie_needs_round'])
            # logger.debug(nrrc[result]['comments'][comment]['tag_ids_need_round'])
            # logger.debug(nrrc[result]['comments'][comment]['tonal_type_needs_round'])
        nrrc[result]['markup_possible'] = markup_possible
        nrrc[result]['marked_up'] = is_result_marked_up(result, expert_id)
        # TODO turn off in production
        for comment in result.comment_set.all():
            make_decision(comment)
    return nrrc


def get_need_round_results_comments(comment, expert_id):
    tags = Tag.objects.all()
    comments_given = False
    specie_needs_round, tonal_type_needs_round, allowed_tag_list = get_allowed(comment, expert_id)

    if specie_needs_round:
        comments_given = True
    elif tonal_type_needs_round:
        comments_given = True
    else:
        for tag in allowed_tag_list:
            if tag:
                comments_given = True

    ret = {
        'specie_needs_round': specie_needs_round,
        'tag_ids_need_round': [tag.name for i, tag in enumerate(tags) if allowed_tag_list[i]],
        'tonal_type_needs_round': tonal_type_needs_round}

    return ret


def most_frequent(List):
    if len(List) <= 0:
        return None
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i
    if counter >= 2:
        return num
    else:
        return None


# def lol():
#     comments = Comment.objects.all()
#     for comment in comments:
#         make_decision(comment)


def make_decision(comment):
    # logger.debug(comment)
    comment_rounds = CommentRound.objects.filter(comment=comment)
    species = Specie.objects.all()
    comment_rounds_species = [comment_round.specie for comment_round in comment_rounds]
    comment_rounds_tonal_types = [comment_round.tonal_type for comment_round in comment_rounds]
    specie_decision = most_frequent(comment_rounds_species)
    # logger.debug(specie_decision)

    if specie_decision is not None:
        comment.specie = specie_decision
    tonal_type_decision = most_frequent(comment_rounds_tonal_types)
    if tonal_type_decision is not None:
        comment.tonal_type = tonal_type_decision
    # logger.debug(tonal_type_decision)

    tags = Tag.objects.all()
    comment_rounds_tags = list(chain(*[comment_round.commentroundtags_set.all() for comment_round in comment_rounds]))
    # logger.debug(comment_rounds_tags)
    comment_tags = [comment_tag.tag for comment_tag in comment.commenttags_set.all()]
    for tag in tags:
        tag_decision = most_frequent([t.is_present for t in comment_rounds_tags if t.tag == tag])
        # logger.debug(tag_decision)
        if tag_decision is not None and tag not in comment_tags:
            CommentTags.objects.create(tag=tag, comment=comment, is_present=tag_decision)
    comment.save()
