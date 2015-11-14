from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import url, patterns

logger = logging.getLogger(__name__)


urlpatterns = patterns('website.apps.salesbro.views',
    url(r'^tickets/$', 'ticket_list', name='ticket_list'),
    url(r'^tickets/(?P<slug>[a-z0-9-]+)/$', 'ticket_detail', name='ticket_detail'),

    url(r'^salesbro/portal/$', 'portal_logon', name='portal_logon'),
    url(r'^salesbro/portal/items/$', 'portal_item', name='portal_item'),
    url(r'^salesbro/portal/cart/$', 'portal_cart', name='portal_cart'),
    url(r'^salesbro/portal/checkout/$', 'portal_checkout', name='portal_checkout'),
)
