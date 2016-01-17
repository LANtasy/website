from django.conf.urls import patterns, url


urlpatterns = patterns('website.apps.badgebro.views',
    url(r'^badge-print/(?P<pk>\d+)/$', 'badge_print', name='print'),
)
