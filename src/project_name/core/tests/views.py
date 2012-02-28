from django.conf import settings
from django.test import TestCase

class LoginRequiredMixinTest(TestCase):
    """
    Tests for the core.views.LoginRequiredMixin
    """

    urls = 'core.tests.urls'

    def _assertRedirectsToLogin(self, response):
        self.assertEquals(response.status_code, 302)
        login_url = "http://testserver%s?next=/login-required-mixin/" % (
            settings.LOGIN_URL
        )
        self.assertEquals(response._headers['location'][1], login_url)


    def test_get(self):
        """
        Test unauthenticated GET requests
        """
        response = self.client.get('/login-required-mixin/')
        self._assertRedirectsToLogin(response)


    def test_post(self):
        """
        Test unauthenticated POST requests
        """
        response = self.client.post('/login-required-mixin/', {})
        self._assertRedirectsToLogin(response)

