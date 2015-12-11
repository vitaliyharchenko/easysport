from django.conf.urls import url

from .views import login_view, logout_view, register_view, register_confirm

urlpatterns = [
    url(r'^login$', login_view, name='login_view'),
    url(r'^logout$', logout_view, name='logout_view'),
    url(r'^reg$', register_view, name='reg_view'),
    url(r'^confirm/(?P<activation_key>.*.{5,100})$', register_confirm, name='confirm'),
]