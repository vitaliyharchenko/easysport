def only_admin_permissions(request):
    if request and request.user.is_admin:
        return True
    else:
        return False


def admin_organizer_permissions(request):
    if request:
        if request.user.is_admin or request.user.is_organizer:
            return True
        else:
            return False
    else:
        return False


def admin_organizer_responsible_permissions(request):
    if request:
        if request.user.is_admin or request.user.is_organizer or request.user.is_responsible:
            return True
        else:
            return False
    else:
        return False