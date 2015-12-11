from users.models import User


def loggedin_user(request):
    context = {'loggedin': request.user.is_authenticated()}
    try:
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            context['current_user'] = user
        else:
            context['current_user'] = None
    except User.DoesNotExist:
        pass
    return context