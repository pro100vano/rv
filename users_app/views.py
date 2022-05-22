from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login

from events_app.models import EventsModel
from .forms import RegisterForm, ProfileForm, ProceduralSheetForm, AchievementsForm
from .models import ProfileModel, ProceduralSheetModel


def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        return HttpResponseRedirect(reverse_lazy('events:list'))


def info(request):
    return render(request, 'info.html')


def contacts(request):
    return render(request, 'contacts.html')


def basa(request):
    return render(request, 'basa.html')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = ''
    success_url = reverse_lazy('profile')
    request = None

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        auth_login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(UpdateView):
    model = ProfileModel
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    request = None

    def get(self, request, *args, **kwargs):
        self.request = request
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = ProfileModel.objects.get(user=self.request.user)
        return obj


class ChildrenList(ListView):
    model = User
    template_name = 'children_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = User.objects.filter(profilemodel__parent=request.user)
        context = self.get_context_data()
        return self.render_to_response(context)


class ChildCreate(CreateView):
    model = ProfileModel
    form_class = ProfileForm
    template_name = 'child_create.html'
    success_url = reverse_lazy('children')
    parent = None
    request = None

    def post(self, request, *args, **kwargs):
        self.request = request
        self.parent = request.user
        self.object = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user_type='child', parent=self.parent)
        messages.success(self.request,
                         "Автоматически задан пароль: " + str(self.object[1]) + ". Сохраните его в безопасном месте!")
        return super().form_valid(form)


class ChildUpdate(UpdateView):
    model = ProfileModel
    form_class = ProfileForm
    template_name = 'child_profile.html'
    success_url = reverse_lazy('children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedural'] = ProceduralSheetModel.objects.filter(user__profilemodel=self.kwargs.get('pk')).order_by(
            '-date')
        context['likes_events'] = context['object'].user.likes.all()
        context['events_status'] = context['object'].user.achievements.all()
        sports = sum([item.status for item in list(context['object'].user.achievements.filter(event__in=[9, 10, 11]))])
        razvls = sum([item.status for item in list(context['object'].user.achievements.filter(event__in=[0, 2]))])
        tvorchs = sum(
            [item.status for item in list(context['object'].user.achievements.filter(event__in=[3, 4, 5, 6, 7, 8]))])
        context['sport'] = sports
        context['razvl'] = razvls
        context['tvorch'] = tvorchs
        return context


class Children(ListView):
    model = User
    template_name = 'children/list.html'
    paginate_by = 10
    queryset = User.objects.filter(groups__name="Ребенок")


def child_search(request):
    if 'child_search' in request.GET and request.GET['child_search']:
        children1 = list(User.objects.filter(first_name__iexact=request.GET['child_search'], groups__name="Ребенок"))
        children2 = list(User.objects.filter(last_name__iexact=request.GET['child_search'], groups__name="Ребенок"))

        children = children1 + children2
        return render(
            request,
            'children/search.html',
            {
                "children": children
            }
        )

    return HttpResponseRedirect('/children/')


class ChildDetail(UpdateView):
    model = ProfileModel
    form_class = ProfileForm
    template_name = 'children/child.html'
    success_url = reverse_lazy('all_children')
    request = None
    kwargs_pk = None

    def get(self, request, *args, **kwargs):
        self.request = request
        self.kwargs_pk = kwargs.get('pk')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = ProfileModel.objects.get(pk=self.kwargs_pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedural'] = ProceduralSheetModel.objects.filter(user__profilemodel=self.kwargs.get('pk')).order_by(
            '-date')
        context['likes_events'] = context['object'].user.likes.all()
        context['events_status'] = context['object'].user.achievements.all()
        return context


class ProceduralSheetCreate(CreateView):
    models = ProceduralSheetModel
    form_class = ProceduralSheetForm
    template_name = 'procedural/create.html'
    success_url = reverse_lazy('all_children')

    def get_initial(self):
        initial = self.initial.copy()
        initial['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return initial

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Посещение отмечено!")
        return super().form_valid(form)


class AchievementsCreate(CreateView):
    models = EventsModel
    form_class = AchievementsForm
    template_name = 'events/event_create.html'
    success_url = reverse_lazy('all_children')

    def get_initial(self):
        initial = self.initial.copy()
        initial['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return initial

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Посещение отмечено!")
        return HttpResponseRedirect(self.get_success_url())


class ProceduralSheetShow(UpdateView):
    models = ProceduralSheetModel
    form_class = ProceduralSheetForm
    template_name = 'procedural/create.html'
    success_url = reverse_lazy('all_children')

    def get_object(self, queryset=None):
        obj = ProceduralSheetModel.objects.get(pk=self.kwargs.get('pk'))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = ProceduralSheetModel.objects.get(pk=self.kwargs.get('pk')).date
        return context
