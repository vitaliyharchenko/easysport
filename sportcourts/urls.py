# coding=utf-8
"""sportcourts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.forms import EmailField
from django.core.exceptions import ValidationError
from django.contrib import admin, auth
from users.models import User
from rest_framework import routers, serializers, viewsets, permissions, authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token


def isemailvalid(email):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Возвращает по запросу текущего авторизованного пользователя
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def current_user(request):
    if request.user.is_authenticated():
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    raise serializers.ValidationError("There is no any authenticated users")


@api_view(['GET'])
@authentication_classes((authentication.TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent email
            if isemailvalid(email):
                user = auth.authenticate(username=email, password=password)
            else:
                raise serializers.ValidationError("Incorrect credientals")

            if not user:
                raise serializers.ValidationError("Incorrect credientals")
        else:
            raise serializers.ValidationError("Incorrect credientals")

        attrs['user'] = user
        return attrs


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def obtainauthtoken(request, format=None):

    serializer = AuthCustomTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    content = {
        'token': unicode(token.key),
    }

    return Response(content)

# Возвращает по запросу текущего авторизованного пользователя
# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def login(request):
#     if request.user.is_authenticated():
#         raise serializers.ValidationError("Already login")
#     email = request.POST["email"]
#     password = request.POST["password"]
#     user = auth.authenticate(username=email, password=password)
#     if not user:
#         raise serializers.ValidationError("Incorrect credientals")
#     else:
#         auth.login(request, user)
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^current/$', current_user),
    url(r'^example/$', example_view),
    url(r'^token/$', obtainauthtoken),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
