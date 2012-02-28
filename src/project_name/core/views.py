from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

class LoginRequiredMixin(View):
    """
    Login Required mixin
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

