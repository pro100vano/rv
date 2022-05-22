from django.urls import path

from events_app.views import EventsListView, like_event

app_name = 'events'

urlpatterns = [
    path('events/', EventsListView.as_view(), name='list'),
    path('events/like/<int:pk>', like_event, name='like'),
]
