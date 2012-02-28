from django.conf.urls.defaults import patterns, url
from django.template import RequestContext
from django.shortcuts import render_to_response

from core.context_processors import is_production
from core.views import LoginRequiredMixin

# Views
def is_production_test_view(request):
    return render_to_response('context_processors/is_production.html',
        RequestContext(request, {}, processors=[is_production]))


class LoginRequiredView(LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Fail, should not hit this method')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Fail, should not hit this method')

# Urls
urlpatterns = patterns('',
    url(r'^is_production/$', is_production_test_view),
    url(r'^login-required-mixin/$', LoginRequiredView.as_view()),
)

