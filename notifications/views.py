# coding=utf-8
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.http import require_POST
from .models import Notification
import json


# Create your views here.
@require_POST
def notification_read(request):
    Notification.objects.filter(user_id=request.user.id, read=0).update(read=1)
    response = {'result': 'OK'}
    if request.is_ajax():
        return HttpResponse(json.dumps(response), content_type="application/json")


@require_POST
def notification_delete(request):
    if request.POST['notification_id']:
        notification_id = request.POST['notification_id']
    else:
        notification_id = 0

    if notification_id != 0:
        Notification.objects.filter(pk=notification_id, user_id=request.user.id).update(read=2)
        response = {'result': 'OK'}
    else:
        Notification.objects.filter(user_id=request.user.id, read=1).update(read=2)
        Notification.objects.filter(user_id=request.user.id, read=0).update(read=2)
        response = {'result': 'OK'}
    if request.is_ajax():
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('index')