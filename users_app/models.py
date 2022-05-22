from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name="parent", blank=True, null=True,
                               default=None)
    avatar = models.FileField()

    def __str__(self):
        return "Профиль: " + str(self.user.username)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ProceduralSheetModel(models.Model):
    expressed = 0
    weak = 1
    is_absent = 2
    OOE_CHOICE = (
        (expressed, "Выраженный"),
        (weak, "Слабый"),
        (is_absent, "Отсутствует"),
    )
    allowed = 0
    limited = 1
    not_allowed = 2
    TYPE_CHOICE = (
        (allowed, "Разрешены"),
        (limited, "Ограничены"),
        (not_allowed, "Не разрешены"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    zakl = models.TextField("Заключение врача специалиста")
    dlii = models.TextField("Данные лабараторно-инструментальных исследований")
    ooe = models.IntegerField("Оценка оздоровительного эффекта", choices=OOE_CHOICE, default=0)
    doz = models.TextField("Диагноз основного заболевания")
    dsz = models.TextField("Диагноз сопутствующих заболеваний")
    sport = models.IntegerField("Спортивные игры", choices=TYPE_CHOICE, default=0)
    excursions = models.IntegerField("Экскурсии", choices=TYPE_CHOICE, default=0)
    kpr = models.TextField("Климатолечение по режиму")
    dr = models.TextField("Климатолечение по режиму")
    diet = models.TextField("Климатолечение по режиму")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Профиль: " + str(self.user.username)

    class Meta:
        verbose_name = 'Процедурный лист'
        verbose_name_plural = 'Процедурные листы'


class AchievementsModel(models.Model):
    concert = 0
    sbor = 1
    plyaj = 2
    tematika = 3
    video = 4
    photo = 5
    graphic = 6
    blog = 7
    suvenir = 8
    football = 9
    shahmati = 10
    voleyball = 11
    EVENT_CHOICE = (
        (concert, "Концерты звезд"),
        (sbor, "Общие сборы"),
        (plyaj, "Пляжная анимация"),
        (tematika, "Тематические дни"),
        (video, "Видеосъемка и постобработка"),
        (photo, "Художественная фотография, ретушь"),
        (graphic, "Графика, дизайн"),
        (blog, "Блогинг, основы журналистики"),
        (suvenir, "Создание сувениров"),
        (football, "Футбол"),
        (shahmati, "Шахматы"),
        (voleyball, "Волейбол"),
    )
    allowed = 0
    limited = 1
    not_allowed = 2

    user = models.ForeignKey(User, related_name='achievements', on_delete=models.CASCADE)
    event = models.IntegerField('Мероприятие', choices=EVENT_CHOICE, default=0)
    status = models.IntegerField("Оценка", default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Оценка: " + str(self.user.username)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'



