from django.shortcuts import render
from pages.views import index_view


# Create your views here.
def events_view(request):
    context = dict()
    if not request.user.is_authenticated():
        return index_view(request)
    else:
        return render(request, 'events.html', context)