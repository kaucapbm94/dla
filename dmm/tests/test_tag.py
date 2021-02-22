from ..helpers import get_common_tags, get_specific_tags
import datetime
import logging
from django.test import TestCase
logger = logging.getLogger(__name__)


class TagHelpersTests(TestCase):

    def test_get_common_tags(self):
        self.assertIsNotNone(get_common_tags())

    def test_get_specific_tags(self):
        self.assertIsNotNone(get_specific_tags())
