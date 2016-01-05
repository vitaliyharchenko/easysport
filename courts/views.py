from django.shortcuts import render
from .models import Court
import json
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def courts_view(request):
    try:
        query = request.GET.__getitem__('q')
        courts = Court.objects.filter(title__icontains=query) | Court.objects.filter(description__icontains=query)
        context = {'courts': courts, 'query': query}
    except KeyError:
        courts = Court.objects.all()
        context = {'courts': courts}

    courts_list = courts.values_list('id', 'title', 'description',
                                     'place__latitude', 'place__longitude',
                                     'place__fulladdress')
    context['map_data'] = json.dumps(list(courts_list), cls=DjangoJSONEncoder)
    return render(request, 'courts.html', context)


def court_view(request, court_id):
    court = Court.objects.get(id=court_id)
    context = {'court': court}
    court.views += 1
    court.save()
    return render(request, 'court.html', context)
