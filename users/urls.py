from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^reg$', views.register_view, name='reg_view'),
    url(r'^vkreg$', views.vk_reg, name='vk_reg'),
    url(r'^confirm/(?P<activation_key>.*.{5,100})$', views.register_confirm, name='confirm'),
    url(r'^update$', views.user_update_view, name="user_update_view"),
    url(r'^changepass$', views.changepass, name="changepass"),
    url(r'^unsetvkid$', views.unsetvkid, name="unsetvkid"),
    url(r'^unsetfbid$', views.unsetfbid, name="unsetfbid"),

    url(r'^resetpass$', views.resetpass, name="resetpass"),

    url(r'^user/(?P<user_id>\d+)$', views.user_view, name='user_view'),
    url(r'^users$', views.users_view, name='users_view'),
]