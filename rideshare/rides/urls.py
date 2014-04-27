from django.conf.urls import patterns, url

from rides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome')
)