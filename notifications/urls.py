from django.conf.urls import patterns, url
import views


urlpatterns = patterns('notifications',
                       url(r'^notifications/read$', views.notification_read, name='read'),
                       url(r'^notifications/delete$', views.notification_delete, name='delete'),
                       )