from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from events_app.models import EventsModel


def like_event(request, **kwargs):
    event = EventsModel.objects.get(pk=kwargs.get('pk'))
    if request.user in list(event.like.all()):
        event.like.remove(request.user)
    else:
        event.like.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class EventsListView(ListView):
    model = EventsModel
    template_name = 'list.html'
    paginate_by = 10
    queryset = EventsModel.objects.filter(date__gte=datetime.today()).order_by('date')
