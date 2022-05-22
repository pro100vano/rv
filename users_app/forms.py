import random
import string
from crispy_forms.layout import Layout, Row, Div, Submit, Field, HTML, Hidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms

from public.forms import BaseModelForm
from users_app.models import ProfileModel, ProceduralSheetModel, AchievementsModel


class RegisterForm(BaseModelForm, UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True
        self.base_fields['username'].help_text = ''

        self.base_fields['username'].label = ''
        self.base_fields['email'].label = ''
        self.base_fields['password1'].label = ''
        self.base_fields['password2'].label = ''

        self.helper.layout = Layout(
            Field('username', placeholder="Пользователь", css_class='my-2 w-100 form-control'),
            Field('email', placeholder="E-mail", css_class='my-2 w-100 form-control'),
            Field('password1', placeholder="Пароль", css_class='my-2 w-100 form-control'),
            Field('password2', placeholder="Подтверждение пароля", css_class='my-2 w-100 form-control'),
            Div(Submit('save', 'Зарегистрироваться', css_class='button btn btn-info btn-block'), css_class='w-100')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='Родитель'))
            ProfileModel.objects.create(user=user)
        return user


class ProfileForm(BaseModelForm):
    avatar = forms.ImageField(label="Аватар", required=False)
    username = forms.CharField(label="Пользователь")
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="Имя", required=False)
    last_name = forms.CharField(label="Фамилия", required=False)

    class Meta:
        model = ProfileModel
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs['instance'] is not None:
            instance = kwargs.pop('instance')

            self.fields['username'].initial = instance.user.username
            self.fields['username'].disabled = True

            self.fields['email'].initial = instance.user.email
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name

        self.helper.layout = Layout(
            Row(
                Div(
                    HTML(
                        '{% if form.username.value is not None and form.avatar.value != "" %}' + \
                        '<img class="w-50" src="/media/{{ form.avatar.value }}">' + \
                        '{% endif %}'
                    ),
                    Field('avatar', css_class='my-2 w-100 form-control'),
                    css_class='col-md-3'
                ),
                Div(
                    Field('username', css_class='my-2 w-100 form-control'),
                    Field('email', css_class='my-2 w-100 form-control'),
                    Field('first_name', css_class='my-2 w-100 form-control'),
                    Field('last_name', css_class='my-2 w-100 form-control'),

                    css_class='col-md-9'
                )
            ),
            Row(Div(Submit('save', 'Сохранить', css_class='button btn btn-info'), css_class='col-auto ml-auto'))
        )

    def save(self, commit=True, user_type=None, parent=None):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile = ProfileModel.objects.get_or_create(user=user)[0]
            profile.avatar = self.cleaned_data['avatar']
            profile.save()
        except Exception:
            if user_type == 'child':
                letters = string.ascii_lowercase + string.ascii_uppercase
                password = ''.join(random.choice(letters) for i in range(10))
                user = User.objects.create_user(
                    self.cleaned_data['username'],
                    self.cleaned_data['email'],
                    password
                )
                user.first_name = self.cleaned_data['first_name']
                user.last_name = self.cleaned_data['last_name']
                user.save()
                user.groups.add(Group.objects.get(name='Ребенок'))
                profile = ProfileModel.objects.create(user=user)
                profile.avatar = self.cleaned_data['avatar']
                profile.parent = parent
                profile.save()
                return user, password
            else:
                raise

        return user


class ProceduralSheetForm(BaseModelForm):
    username = forms.CharField(label="Пользователь")
    user_id = forms.IntegerField(label="Пользователь", required=False)

    class Meta:
        model = ProceduralSheetModel
        fields = ('id', 'zakl', 'dlii', 'ooe', 'doz', 'dsz', 'kpr', 'dr', 'diet', 'sport', 'excursions',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        if 'user' in initial:
            self.fields['user_id'].initial = initial['user'].id
            self.fields['username'].initial = initial['user'].first_name + " " + initial['user'].last_name
        else:
            self.fields['username'].initial = kwargs['instance'].user.first_name + " " + kwargs[
                'instance'].user.last_name
            self.fields['zakl'].disabled = True
            self.fields['dlii'].disabled = True
            self.fields['ooe'].disabled = True
            self.fields['doz'].disabled = True
            self.fields['dsz'].disabled = True
            self.fields['kpr'].disabled = True
            self.fields['sport'].disabled = True
            self.fields['excursions'].disabled = True
            self.fields['dr'].disabled = True
            self.fields['diet'].disabled = True
        self.fields['username'].disabled = True

        layout_1 = Layout(
            Field('user_id', type="hidden"),
            Field('username', css_class='my-2 w-100 form-control'),
            Field('zakl', rows=3, css_class='my-2 w-100 form-control'),
            Field('dlii', rows=3, css_class='my-2 w-100 form-control'),
            Field('ooe', css_class='my-2 w-100 form-control'),
            Field('doz', rows=3, css_class='my-2 w-100 form-control'),
            Field('dsz', rows=3, css_class='my-2 w-100 form-control'),
            Field('kpr', rows=3, css_class='my-2 w-100 form-control'),
            Field('sport', css_class='my-2 w-100 form-control'),
            Field('excursions', css_class='my-2 w-100 form-control'),
            Field('dr', rows=3, css_class='my-2 w-100 form-control'),
            Field('diet', rows=3, css_class='my-2 w-100 form-control'),

        )
        layout_2 = Layout(
            Row(Div(Submit('save', 'Отметить', css_class='button btn btn-info'), css_class='col-auto ml-auto'))
        )

        if 'user' in initial:
            self.helper.layout = Layout(layout_1, layout_2)
        else:
            self.helper.layout = Layout(layout_1)

    def save(self, commit=True):
        try:
            user = User.objects.get(pk=self.cleaned_data['user_id'])
            sheet = ProceduralSheetModel.objects.create(
                user=user,
                zakl=self.cleaned_data['zakl'],
                dlii=self.cleaned_data['dlii'],
                ooe=self.cleaned_data['ooe'],
                doz=self.cleaned_data['doz'],
                dsz=self.cleaned_data['dsz'],
                dr=self.cleaned_data['dr'],
                diet=self.cleaned_data['diet'],
                sport=self.cleaned_data['sport'],
                excursions=self.cleaned_data['excursions'],
            )
        except Exception:
            raise
        return sheet


class AchievementsForm(BaseModelForm):
    username = forms.CharField(label="Пользователь")
    user_id = forms.IntegerField(label="Пользователь", required=False)
    status = forms.IntegerField(label="Оценка", min_value=1, max_value=3)
    event = forms.ChoiceField(label="Мероприятие", choices=AchievementsModel.EVENT_CHOICE)

    class Meta:
        model = AchievementsModel
        fields = ('id', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial')

        if 'user' in initial:
            self.fields['user_id'].initial = initial['user'].id
            self.fields['username'].initial = initial['user'].first_name + " " + initial['user'].last_name

        self.fields['username'].disabled = True

        layout_1 = Layout(
            Field('user_id', type="hidden"),
            Field('username', css_class='my-2 w-100 form-control'),
            Field('event', css_class='my-2 w-100 form-control'),
            Field('status',  css_class='my-2 w-100 form-control'),
        )
        layout_2 = Layout(
            Row(Div(Submit('save', 'Отметить', css_class='button btn btn-info'), css_class='col-auto ml-auto'))
        )

        if 'user' in initial:
            self.helper.layout = Layout(layout_1, layout_2)
        else:
            self.helper.layout = Layout(layout_1)

    def save(self, commit=True):
        try:
            user = User.objects.get(pk=self.cleaned_data['user_id'])
            achievement = AchievementsModel.objects.create(
                user=user,
                event=self.cleaned_data['event'],
                status=self.cleaned_data['status'],
            )
        except Exception:
            raise
        return achievement
