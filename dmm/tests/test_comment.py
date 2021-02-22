from django.test import TestCase
from dmm.helpers.comment import comment_tag_is_finished
from ..models import Comment, Tag
import logging
logger = logging.getLogger(__name__)


class CommentTestCase(TestCase):
    fixtures = ['dump.json']

    def test_comment_tag_is_finished(self):
        comm = Comment.objects.get(id='18426c05-3dd1-472b-8f98-fe13db5dbeba')
        tag = Tag.objects.get(id=1)

        # get_info()
        logger.debug(comment_tag_is_finished(comm, tag))
