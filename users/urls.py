from django.conf.urls import include, url
from django.contrib import admin

from .views import login_view, logout_view

urlpatterns = [
    url(r'^login/$', login_view, name='login_view'),
    url(r'^logout/$', logout_view, name='logout_view'),
]