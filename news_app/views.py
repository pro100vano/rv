from django.shortcuts import render
from django.views.generic import ListView

from news_app.models import NewsModel


class NewsList(ListView):
    model = NewsModel
    queryset = NewsModel.objects.all().order_by('-date_created')
    template_name = 'news/list.html'
    paginate_by = 10
