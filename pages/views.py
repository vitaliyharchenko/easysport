from django.shortcuts import render


# Create your views here.
def index_view(request):
    if request.user.is_authenticated():
        #TODO: redirect to events
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')