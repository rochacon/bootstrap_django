from django.http import HttpResponse
try:
    import json
except ImportError:
    from django.utils import simplejson as json

# Response to JSON shortcut
class HttpResponseJSON(HttpResponse):
    def __init__(self, content='', mimetype='application/json', *args, **kwargs):
        if content:
            content = json.dumps(content)
        super(HttpResponseJSON, self).__init__(content, mimetype, *args, **kwargs)

