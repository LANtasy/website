from django.conf.urls import patterns, url, include


urlpatterns = patterns('website.apps.badgebro.api.v1.views',
    url(r'^badge/authenticate/$', 'auth_badge', name='auth_badge'),
)
