from ..models import CommentRound


def tonal_type_is_present(comment, tonal_type):
    return True if CommentRound.objects.filter(comment=comment, tonal_type=tonal_type).count() >= 1 else False
