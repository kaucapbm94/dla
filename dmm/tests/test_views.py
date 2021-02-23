from django.test import TestCase, Client
from django.test import Client
import logging
logger = logging.getLogger(__name__)


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

    def test_start_get(self):
        response = self.c.get('')
        logger.debug(response)
        self.assertEquals(response.status_code, 200)

        # self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_list_GET(self):
        response = self.c.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')
