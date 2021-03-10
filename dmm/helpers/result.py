from ..models import Tag
import logging
logger = logging.getLogger(__name__)


def is_result_marked_up(result, expert_id):
    is_marked_up = True
    tags = Tag.objects.all()
    for comment in result.comment_set.all():
        # for tag in tags:
        #     if tag not in comment.commenttags_set.all():
        #         is_marked_up = False
        if comment.specie is None or comment.tonal_type is None:
            is_marked_up = False
            break

    return is_marked_up
