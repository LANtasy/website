from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import patterns, url

logger = logging.getLogger(__name__)

urlpatterns = patterns('website.apps.userbro.views',
    url(r'^$', 'user_detail', name='user_detail'),
    url(r'^change-password/$', 'change_password', name='change_password'),
    url(r'^release-badge/$', 'user_release_badge', name='user_release_badge'),
)
