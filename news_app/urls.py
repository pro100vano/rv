from django.urls import path

from news_app.views import NewsList

app_name = 'news'

urlpatterns = [
    path('news/', NewsList.as_view(), name="list"),
]
