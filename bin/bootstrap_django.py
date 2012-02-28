#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import shutil
import string
import sys

from django.conf import settings
from django.template.loader import render_to_string


# Settings
BOOTSTRAP_ROOT = os.path.dirname(os.path.abspath(__file__))
BOOTSTRAP_TEMPLATE_DIR = os.path.join(BOOTSTRAP_ROOT, 'templates')

settings.configure(
	TEMPLATE_DIRS=(BOOTSTRAP_TEMPLATE_DIR,),
	DEFAULT_CHARSET='UTF-8'
)

# Bootstrap Django project
def get_secret():
	return ''.join(random.choice(string.letters + string.digits +
		string.punctuation) for x in range(60))


def touch_new_file(dest):
	with open(dest, 'w') as f:
		f.write('\n')


if __name__ == '__main__':

	if len(sys.argv) < 2:
	    print u'Usage: {0} project_name [destination_path]'.format(sys.argv[0])
	    sys.exit(1)

	project_name = sys.argv[1].lower()

	# Create new Django project root folder
	if len(sys.argv) == 3:
		base_path = sys.argv[2]

	else:
		base_path = os.path.join(BOOTSTRAP_ROOT, '..', 'src', project_name)

	# create project path
	if os.path.exists(base_path):
		print u'Project folder already exists. Aborting.'
		sys.exit(1)

	os.mkdir(base_path)

	if not os.path.exists(os.path.join(base_path, '__init__.py')):
		touch_new_file(os.path.join(base_path, '__init__.py'))

	# Override manage script
	manage_script = os.path.join(base_path, 'manage.py')
	with open(manage_script, 'w') as s:
		rendered_manage = render_to_string('manage.py', {
			'project_name': project_name
		})
		s.write(rendered_manage)
	os.chmod(manage_script, 0744)

	# Override settings file and replace config holders
	with open(os.path.join(base_path, 'settings.py'), 'w') as s:
		rendered_settings = render_to_string('settings.py', {
			'project_name': project_name,
			'secret': get_secret()
		})
		s.write(rendered_settings)

	# Copy core app
	core_app = os.path.join(base_path, 'core')
	if not os.path.exists(core_app):
		shutil.copytree(os.path.join(BOOTSTRAP_TEMPLATE_DIR, 'core'), core_app)

	print '{0} criado com sucesso.'.format(project_name)
