from django.shortcuts import render, redirect
from users.models import User


# Create your views here.
def index_view(request):
    users = User.objects.filter(pk__in=[1, 94, 90, 41, 29, 28, 14, 842])
    return render(request, 'index.html', {'users': users})


def contacts_view(request):
    return render(request, 'contacts.html')


def stats_view(request):
    return render(request, 'stats.html')
