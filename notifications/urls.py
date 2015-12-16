from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^notification/read$', views.notification_read, name='notification_read'),
    url(r'^notification/delete$', views.notification_delete, name='notification_delete'),
]