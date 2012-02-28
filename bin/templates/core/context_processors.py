from django.conf import settings

def is_production(request):
    """
    Context processor for production context variable 
    """
    return {'is_production': not settings.DEBUG}

