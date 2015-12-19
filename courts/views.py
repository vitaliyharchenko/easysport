from django.shortcuts import render
from .models import Court


# Create your views here.
def courts_view(request):
    try:
        query = request.GET.__getitem__('q')
        courts = Court.objects.filter(title__icontains=query) | Court.objects.filter(description__icontains=query)
        context = {'courts': courts, 'query': query}
    except KeyError:
        context = {'courts': Court.objects.all()}
    return render(request, 'courts.html', context)


def court_view(request, court_id):
    court = Court.objects.get(id=court_id)
    context = {'court': court}
    court.views += 1
    court.save()
    return render(request, 'court.html', context)
