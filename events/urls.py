from django.conf.urls import url

from .views import events_view

urlpatterns = [
    url(r'^$', events_view, name='index_view'),
]