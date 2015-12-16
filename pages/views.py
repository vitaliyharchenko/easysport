from django.shortcuts import render, redirect


# Create your views here.
def index_view(request):
    if request.user.is_authenticated():
        return redirect('games_view')
    else:
        return render(request, 'index.html')


def contacts_view(request):
    return render(request, 'contacts.html')