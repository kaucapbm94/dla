from django.test import TestCase
from dmm.views.result import createResult
from ..models import Comment, Tag, Result
import logging
import json
logger = logging.getLogger(__name__)


class ResultTestCase(TestCase):
    fixtures = ['dump.json']

    def test_create_result(self):
        request = "<QueryDict: {'csrfmiddlewaretoken': ['vne12GRrwZkLNRzGj4xbyd8xIJhOxMgH9nngyQp0QalOK0VxVsdiLPucB9dRFt4X'], 'text': ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'], 'url': ['https://github.com/'], 'title': ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'], 'date': ['2021-02-22T11:37'], 'content_type': ['1'], 'expert': ['f9f5b2d8-0947-4bbc-9931-3faa839001e5'], 'language_type': ['1'], 'resource_type': ['1'], 'comment_set-TOTAL_FORMS': ['1'], 'comment_set-INITIAL_FORMS': ['0'], 'comment_set-MIN_NUM_FORMS': ['0'], 'comment_set-MAX_NUM_FORMS': ['1'], 'comment_set-0-text': ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed elementum sem ac magna suscipit, non.'], 'comment_set-0-author_url': ['https://github.com/'], 'comment_set-0-date': ['2021-02-22T11:37'], 'comment_set-0-clarification': ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.'], 'comment_set-0-expert': ['00d52d59-b11d-4aa2-8f12-f1fda93857b5'], 'comment_set-0-language_type': ['1'], 'comment_set-0-resource_type': ['1'], 'comment_set-0-specie': ['1'], 'comment_set-0-tonal_type': ['1'], 'comment_set-0-tags': ['1', '2'], 'comment_set-0-result': [''], 'Submit': ['Submit']}>"
        createResult(request)
        # comm = Comment.objects.get(id='18426c05-3dd1-472b-8f98-fe13db5dbeba')
        # tag = Tag.objects.get(id=1)

        # # get_info()
        # logger.debug(comment_tag_is_finished(comm, tag))
