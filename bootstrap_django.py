#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import string
import sys

from django.conf import settings
from django.template.loader import render_to_string


# Django setup
base_path = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    TEMPLATE_DIRS=[base_path],
    DEFAULT_CHARSET='UTF-8'
)

### Configurations, where the fun is planned. :)
#
# Set here the context variables for the configurations rendering
context = {
    # The base path of the project, where the bootstrap.py script lives
    'base_path': base_path,

    # The domain to be used in the NGINX configurations
    'domain': 'localhost',

    # The project name, this should be a valid Python module name
    # (e.g. valid Django project name, lowercase without - or . )
    'project_name': None,

    # The user id that will run the NGINX e uWSGI daemons
    'uid': 'www-data',

    # uWSGI INI configuration file, this is only used at the init.d script
    # rendering
    'uwsgi_inifile': os.path.join(base_path, 'etc', 'uwsgi', 'uwsgi.ini'),

    # uWSGI PID file, this used at the etc/init.d/project_name.sh and
    # etc/uwsgi/uwsgi.ini, configs rendering
    'uwsgi_pidfile': os.path.join(base_path, 'pid', 'uwsgi.pid'),

    # Project Virtualenv path, this is only used at the uwsgi.ini config
    # rendering
    'virtualenv_path': os.path.join(base_path, '.venv')
}

# Utilities
def generate_secret():
    """
    Generate a 60 character random string for the SECRET_KEY
    """
    return ''.join(random.choice(string.letters + string.digits +
        string.punctuation) for x in range(60))


def render_settings_file(file_path, context={}, mode=None):
    """
    Render a settings file in place
    """
    rendered = render_to_string(file_path, context)
    with open(file_path, 'w') as f:
        f.write(rendered)

    if mode is not None:
        os.chmod(file_path, mode)


# Main code
if __name__ == '__main__':

    project_name = context['project_name']

    if not project_name:
        print u'Setup the configuration dict to start. (Hint: go to line 20)'
        sys.exit(1)

    # render settings file
    render_settings_file(os.path.join('src', 'project_name', 'settings.py'), context)
    os.rename(os.path.join('src', 'project_name'),
              os.path.join('src', project_name))

    # render etc/init.d script
    render_settings_file(os.path.join('etc', 'init.d', 'project_name.sh'), context, 0744)
    os.rename(os.path.join('etc', 'init.d', 'project_name.sh'),
              os.path.join('etc', 'init.d', '%s.sh' % project_name))

    # render etc/nginx/nginx.conf
    render_settings_file(os.path.join('etc', 'nginx', 'nginx.conf'), context)

    # render etc/nginx/project_name.conf
    render_settings_file(os.path.join('etc', 'nginx', 'project_name.conf'), context)
    os.rename(os.path.join('etc', 'nginx', 'project_name.conf'),
              os.path.join('etc', 'nginx', '%s.conf' % project_name))

    # render etc/uwsgi/uwsgi.ini
    render_settings_file(os.path.join('etc', 'uwsgi', 'uwsgi.ini'), context)

    # Success!
    print '''%(project_name)s bootstrapped successfully.
    Delete this script:
        git rm bootstrap.py

    And set your git upstream remote:
        git remote set-url origin git@github.com:rochacon/bootstrap_django

    Commit the changes and start writing code!
    ''' % {'project_name': project_name}
