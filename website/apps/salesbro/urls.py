from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import url, patterns

from website.apps.salesbro import views

logger = logging.getLogger(__name__)


urlpatterns = patterns('website.apps.salesbro.views',
    url(r'^tickets/$', 'ticket_list', name='ticket_list'),
    url(r'^tickets/(?P<slug>[a-z0-9-]+)/$', 'ticket_detail', name='ticket_detail'),

    url(r'^vendor/$', views.VendorLogon.as_view(), name='vendor_logon'),
    url(r'^vendor/cart/$', views.VendorCart.as_view(), name='vendor_cart'),
    url(r'^vendor/checkout/$', views.VendorCheckout.as_view(), name='vendor_checkout'),
)
