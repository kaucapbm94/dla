from ..models import Tag

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


def get_specific_tags():
    return Tag.objects.filter(is_common=False)


def get_common_tags():
    return Tag.objects.filter(is_common=True)
