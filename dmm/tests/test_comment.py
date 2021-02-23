from django.test import TestCase
from dmm.helpers.comment import tag_is_present
from ..models import Comment, Tag
import logging
logger = logging.getLogger(__name__)


class CommentTestCase(TestCase):
    fixtures = ['dump.json']

    # python3 manage.py test dmm.tests.CommentTestCase.test_tag_is_present
    def test_tag_is_present(self):
        comm = Comment.objects.get(id='18426c05-3dd1-472b-8f98-fe13db5dbeba')
        tag = Tag.objects.get(id=1)

        # get_info()
        logger.debug(tag_is_present(comm, tag))
