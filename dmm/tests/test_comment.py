from django.test import TestCase
from dmm.helpers import tag_is_present, get_allowed, make_decision
from ..models import *
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

    # python3 manage.py test dmm.tests.CommentTestCase.test_get_allowed
    def test_get_allowed(self):
        logger.debug(Tag.objects.all())
        logger.debug(Specie.objects.all())
        logger.debug(TonalType.objects.all())
        result_id = 'd1a49558-805b-4376-8afc-72587fdd46c9'
        comments = Comment.objects.filter(result_id=result_id)
        expert_id = 'f9f5b2d8-0947-4bbc-9931-3faa839001e5'

        for comm in comments:
            logger.debug(comm.__dict__)
            logger.debug(get_allowed(comm, expert_id))

    # python3 manage.py test dmm.tests.CommentTestCase.test_make_decision
    def test_make_decision(self):
        comment = Comment.objects.get(id='ddbeaa71-03eb-40d9-881d-d7a62f387e62')
        make_decision(comment)
