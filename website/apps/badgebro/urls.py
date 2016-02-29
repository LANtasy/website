from django.conf.urls import patterns, url


urlpatterns = patterns('website.apps.badgebro.views',
    url(r'^frontdesk/$', 'front_desk', name='front_desk'),
    url(r'^frontdesk/badge/(?P<uid>BA\w{32})/$', 'badge_detail', name='badge_detail'),
    url(r'^frontdesk/badge/(?P<uid>BA\w{32})/upgrade/$', 'badge_upgrade', name='badge_upgrade'),
    url(r'^frontdesk/badge/(?P<uid>BA\w{32})/printed/$', 'badge_printed', name='badge_printed'),
    url(r'^frontdesk/badge/(?P<uid>BA\w{32})/collected/$', 'badge_collected', name='badge_collected'),
    url(r'^frontdesk/badge/(?P<uid>BA\w{32})/print/$', 'badge_print_close', name='badge_print'),

    url(r'^frontdesk/order/(?P<order_pk>\d+)/$', 'badge_order_detail', name='badge_order_detail'),
    url(r'^frontdesk/order/(?P<order_pk>\d+)/badge/(?P<uid>BA\w{32})/upgrade/$', 'badge_order_upgrade', name='badge_order_upgrade'),

    url(r'^badgebro/print/(?P<uid>BA\w{32})/$', 'badge_print', name='print'),
    url(r'^badgebro/(?P<uid>BA\w{32})/difference/(?P<ticket_id>\d+)/$', 'badge_difference', name='badge_difference'),

    url(r'^frontdesk/organize/$', 'organize_conventions', name='organize_conventions'),
    url(r'^frontdesk/organize/(?P<convention>[-\w]+)/badges/$', 'organize_badges', name='organize_badges'),
    url(r'^frontdesk/export/(?P<convention>[-\w]+)/badges/$', 'organize_badges_export', name='organize_badges_export'),
    url(r'^frontdesk/organize/(?P<convention>[-\w]+)/badges/(?P<filter>[-\w]+)/$', 'organize_badges', name='organize_badges'),
    url(r'^frontdesk/export/(?P<convention>[-\w]+)/badges/(?P<filter>[-\w]+)/$', 'organize_badges_export', name='organize_badges_export'),

    url(r'^frontdesk/organize/(?P<convention>[-\w]+)/$', 'organize_events', name='organize_events'),
    url(r'^frontdesk/organize/(?P<convention>[-\w]+)/events/(?P<event>[-\w]+)/$', 'organize_registrations', name='organize_registrations'),
    url(r'^frontdesk/export/(?P<convention>[-\w]+)/events/(?P<event>[-\w]+)/$', 'organize_registrations_export', name='organize_registrations_export'),


)
