from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url('^v1/', include('website.apps.apibro.v1.urls', namespace='api_v1')),
)
