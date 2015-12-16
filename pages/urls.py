from django.conf.urls import url

from .views import index_view, contacts_view

urlpatterns = [
    url(r'^$', index_view, name='index_view'),
    url(r'^contacts$', contacts_view, name='contacts_view'),
]