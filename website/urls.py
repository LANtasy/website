from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from mezzanine.core.views import direct_to_template

from cartridge_stripe.forms import OrderForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Shop URLs.
    url(r'^shop/checkout/$', 'cartridge.shop.views.checkout_steps', name='checkout_steps',
        kwargs=dict(form_class=OrderForm)),
    url(r'^shop/', include('cartridge.shop.urls')),
    url(r'^account/orders/$', 'cartridge.shop.views.order_history', name='shop_order_history'),
    url(r'^zebra/', include('zebra.urls',  namespace="zebra",  app_name='zebra')),
    url(r'^', include('website.apps.salesbro.urls',  namespace='salesbro')),

    # Temporary shop redirect
    url(r'^shop$', RedirectView.as_view(url='tickets/', permanent=False)),

    # Index URL
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='home'),

    # Mezzanine defaults URLs
    (r'^', include('mezzanine.urls')),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
