from django.conf.urls import url

from .views import index_view, contacts_view, stats_view

urlpatterns = [
    url(r'^$', index_view, name='index_view'),
    url(r'^contacts$', contacts_view, name='contacts_view'),
    url(r'^stats$', stats_view, name='stats_view'),
]