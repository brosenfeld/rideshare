from django.conf.urls import patterns, url

from rides import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^eventbrite$', views.eventbrite_permission, name='eventbrite_permission'),
    url(r'^eventbrite/link/', views.eventbrite_link, name='eventbrite_link'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^invalid/$', views.invalid, name='invalid'),
    url(r'^event/(?P<event_id>\d+)/details/$', views.event_details, name='event_details'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^accounts/login/', views.user_login, name='user_login'),
    url(r'^accounts/logout/', views.user_logout, name='user_logout'),
    url(r'^event/(?P<event_id>\d+)/rides/add$', views.ride_add, name='ride_add'),
    url(r'^ride/(?P<ride_id>\d+)/details$', views.ride_details, name='ride_details'),
    url(r'^ride/(?P<ride_id>\d+)/join$', views.ride_join, name='ride_join'),
    url(r'^ride/(?P<ride_id>\d+)/cancel$', views.ride_cancel, name='ride_cancel'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
)
