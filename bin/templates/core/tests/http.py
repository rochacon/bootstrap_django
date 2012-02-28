from django.test import TestCase

from core.http import HttpResponseJSON

class HttpResponseJSONTest(TestCase):
    def test_config_setup(self):
        """
        Test the instance setup 
        """
        response = HttpResponseJSON({'ok': 'ok'})
        self.assertEqual('application/json', response.get('Content-Type', ''))
        self.assertEqual('{"ok": "ok"}', response.content)

