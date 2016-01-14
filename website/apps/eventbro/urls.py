from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import url, patterns

logger = logging.getLogger(__name__)


urlpatterns = patterns('website.apps.eventbro.views',

    url(r'^import/events/$', 'event_import', name='event_import'),
    url(r'^register/$', 'register_redirect', name='register_redirect'),
    url(r'^register/badge/$', 'register_badge', name='register_badge'),
    url(r'^register/events/$', 'register_event', name='register_event'),
    url(r'^register/events/(?P<slug>[-\w]+)/$', 'register_event', name='register_event'),
    url(r'^register/events/(?P<event_slug>[-\w]+)/update/$', 'registration_detail', name='registration_update'),

    url(r'^convention/(?P<slug>[-\w]+)/$', 'convention_detail', name='convention_detail'),
    url(r'^event_type/(?P<slug>[-\w]+)/$', 'event_type_detail', name='event_type_detail'),
    url(r'^event/(?P<slug>[-\w]+)/$', 'event_detail', name='event_detail'),
)
