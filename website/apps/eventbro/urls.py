from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import url, patterns

logger = logging.getLogger(__name__)


urlpatterns = patterns('website.apps.eventbro.views',

    url(r'^register/$', 'register_redirect', name='register_redirect'),
    url(r'^register/badge/$', 'register_badge', name='register_badge'),
    url(r'^register/events/$', 'register_event', name='register_event'),
    url(r'^register/events/(?P<id>\d+)/$', 'register_event', name='register_event'),

    url(r'^register/events/(?P<event_id>\d+)/update/$', 'registration_detail', name='registration_update')
)
