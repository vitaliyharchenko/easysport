from django.conf.urls import url

from .views import login_view, logout_view, register_view, user_update_view, changepass, register_confirm, user_view, users_view

urlpatterns = [
    url(r'^login$', login_view, name='login_view'),
    url(r'^logout$', logout_view, name='logout_view'),
    url(r'^reg$', register_view, name='reg_view'),
    url(r'^confirm/(?P<activation_key>.*.{5,100})$', register_confirm, name='confirm'),
    url(r'^update$', user_update_view, name="user_update_view"),
    url(r'^changepass$', changepass, name="changepass"),

    url(r'^user/(?P<user_id>\d+)$', user_view, name='user_view'),
    url(r'^users$', users_view, name='users_view'),
]