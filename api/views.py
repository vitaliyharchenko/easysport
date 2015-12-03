from django.forms import EmailField
from django.core.exceptions import ValidationError
from django.contrib import auth
from users.models import User
from rest_framework import routers, serializers, viewsets, permissions, authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.
def isemailvalid(email):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


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
        'user': unicode(request.user),
        'auth': unicode(request.auth),
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
@authentication_classes((authentication.TokenAuthentication,))
def obtainauthtoken(request, format=None):

    serializer = AuthCustomTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    content = {
        'token': unicode(token.key),
    }

    return Response(content)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)