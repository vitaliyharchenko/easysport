from users.models import User
from notifications.models import Notification
from django.utils import timezone


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


def notifications(request):
    context = dict()
    query = Notification.objects.filter(user_id=request.user.id, datetime__lte=timezone.now())
    new_count = query.filter(read=0).count()
    read_count = query.filter(read=1).count()
    if new_count:
        new = query.filter(read=0)
        context['notifications_new'] = new
    else:
        new = Notification.objects.none()

    if read_count:
        read = query.filter(read=1)
    else:
        read = Notification.objects.none()

    context['notifications_all'] = new | read

    context['notifications_count'] = new_count + read_count
    return context