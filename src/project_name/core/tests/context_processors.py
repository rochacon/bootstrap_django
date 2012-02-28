import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

class IsProductionContextProcessorTests(TestCase):
    """
    Tests for the core.is_production processor
    """

    urls = 'core.tests.urls'

    def setUp(self):
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(os.path.dirname(__file__), 'templates'),
        )

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS


    def test_is_production_processor(self):
        """
        Test if is_production context is being setted
        """
        response = self.client.get('/is_production/')
        self.assertTrue('is_production' in response.context)
        self.assertTrue(response.context['is_production'])
        self.assertContains(response, 'OK')

