from __future__ import unicode_literals, absolute_import


import os

from fabric.api import env, run, sudo
from fabric.context_managers import hide, cd
from fabric.decorators import roles
from fabric.colors import green, yellow


def production():
    env.name = 'production'
    env.user = 'bcgamer'

    env.roledefs = {
        'webservers': ['www.lantasy.com', ],
        'workers': ['www.lantasy.com', ],
        'beat': ['www.lantasy.com', ],
    }

    env.repo_name = os.getenv('CIRCLE_PROJECT_REPONAME')
    env.branch = os.getenv('CIRCLE_BRANCH')
    env.sha1 = os.getenv('CIRCLE_SHA1')
    env.circle_build_num = os.getenv('CIRCLE_BUILD_NUM')

    env.home = '/home/%(user)s' % env
    env.project_root = '%(home)s/www.lantasy.com/website' % env
    env.venv_path = '%(home)s/www.lantasy.com/env' % env
    env.python_path = '%(venv_path)s/bin/python' % env
    env.settings_module = 'website.settings.%(name)s' % env

    env.build_dir = '%(home)s/builds'

    env.activate = '%(venv_path)s/bin/activate' % env

    env.uwsgi_job = 'lantasy_uwsgi'
    env.celery_worker_job = 'lantasy_worker'
    env.celery_beat_job = 'lantasy_beat'


def success():
    print(green('Success!'))


@roles(['webservers', 'workers', 'beat'])
def deploy():

    env.sha1 = '0b32b2fb1a15f4d4deef54bad557e12ffb78f9d2'

    with cd(env.project_root):

        run('git fetch')
        run('git clean -f -d')
        run('git checkout %(sha1)s' % env)

        run('%(venv_path)s/bin/pip install -r requirements/requirements.txt' % env)
        run('%(venv_path)s/bin/pip install -r requirements/production.txt' % env)

        run('%(venv_path)s/bin/python manage.py migrate' % env)
        run('%(venv_path)s/bin/python manage.py collectstatic --noinput' % env)


    print(yellow('Restarting uWSGI'))
    uwsgi_restart()
    success()

    # print(yellow('Restarting celery workers'))
    # worker_restart()
    # success()
    #
    # print(yellow('Restarting celery beat'))
    # success()


@roles(['webservers', ])
def uwsgi_start():
    with hide('stdout'):
        sudo('supervisorctl status %s' % env.uwsgi_job)


@roles(['webservers', ])
def uwsgi_stop():
    with hide('stdout'):
        sudo('supervisorctl stop %s' % env.uwsgi_job)


@roles(['webservers', ])
def uwsgi_restart():
    with hide('stdout'):
        sudo('supervisorctl restart %s' % env.uwsgi_job)


@roles(['workers', ])
def worker_start():
    with hide('stdout'):
        sudo('supervisorctl start %s' % env.celery_worker_job)


@roles(['workers', ])
def worker_stop():
    with hide('stdout'):
        sudo('supervisorctl stop %s' % env.celery_worker_job)


@roles(['workers', ])
def worker_restart():
    with hide('stdout'):
        sudo('supervisorctl restart %s' % env.celery_worker_job)


@roles(['beat', ])
def beat_start():
    with hide('stdout'):
        sudo('supervisorctl start %s' % env.celery_beat_job)


@roles(['beat', ])
def beat_stop():
    with hide('stdout'):
        sudo('supervisorctl stop %s' % env.celery_beat_job)


@roles(['beat', ])
def beat_restart():
    with hide('stdout'):
        sudo('supervisorctl restart %s' % env.celery_beat_job)

