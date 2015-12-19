def only_admin_permissions(request):
    if request.user and request.user.is_admin:
        return True
    else:
        return False


def admin_organizer_permissions(request):
    if request.user:
        if request.user.is_admin or request.user.is_organizer:
            return True
        else:
            return False
    else:
        return False