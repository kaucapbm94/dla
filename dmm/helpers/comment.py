from ..models import *


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
    tags = Tag.objects.all()
    for result in results:
        # logger.debug(get_comments(result.comment_set.all(), expert_id))
        comments = result.comment_set.all()

        need_round_comments = {}

        comments_given = False

        for comment in comments:
            specie_needs_round, tonal_type_needs_round, allowed_tag_list = get_allowed(comment, expert_id)

            if specie_needs_round:
                comments_given = True
            elif tonal_type_needs_round:
                comments_given = True
            else:
                for tag in allowed_tag_list:
                    if tag:
                        comments_given = True
            if comments_given:
                need_round_comments[comment] = {
                    'specie_needs_round': specie_needs_round,
                    'tag_ids_need_round': [tag.name for i, tag in enumerate(tags) if allowed_tag_list[i]],
                    'tonal_type_needs_round': tonal_type_needs_round}
        if need_round_comments:
            nrrc[result] = need_round_comments

    return nrrc
