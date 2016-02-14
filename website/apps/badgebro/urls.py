from django.conf.urls import patterns, url


urlpatterns = patterns('website.apps.badgebro.views',
    url(r'^frontdesk/$', 'front_desk', name='front_desk'),
    url(r'^frontdesk/(?P<uid>BA\w{32})/$', 'badge_detail', name='badge_detail'),
    url(r'^frontdesk/(?P<uid>BA\w{32})/upgrade/$', 'badge_upgrade', name='badge_upgrade'),
    url(r'^frontdesk/(?P<uid>BA\w{32})/print/$', 'badge_printed', name='badge_printed'),
    url(r'^frontdesk/(?P<uid>BA\w{32})/collect/$', 'badge_collected', name='badge_collected'),

    url(r'^frontdesk/order/(?P<order_pk>\d+)/$', 'badge_order_detail', name='badge_order_detail'),
    url(r'^frontdesk/order/(?P<order_pk>\d+)/badge/(?P<uid>BA\w{32})/upgrade/$', 'badge_order_upgrade', name='badge_order_upgrade'),

    url(r'^badgebro/print/(?P<pk>\d+)/$', 'badge_print', name='print'),
    url(r'^badgebro/(?P<uid>BA\w{32})/difference/(?P<ticket_id>\d+)/$', 'badge_difference', name='badge_difference'),
)
