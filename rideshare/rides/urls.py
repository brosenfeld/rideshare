from django.conf.urls import patterns, url

from rides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^event/(?P<event_id>\d+)/details/$', views.event_details, name='event_details')
)