from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views
from .views import router, current_user, example_view, obtainauthtoken


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^current/$', current_user),
    url(r'^example/$', example_view),
    url(r'^token/$', obtainauthtoken),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]