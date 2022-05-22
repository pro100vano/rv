from django.contrib.auth.models import User
from django.db import models


class EventsModel(models.Model):
    SPORT = 0
    GAME = 1
    MEDICINE = 2
    CREATE = 3
    TYPE_CHOICE = (
        (SPORT, 'Спортивнй'),
        (GAME, 'Развлекательный'),
        (MEDICINE, 'Лечебный'),
        (CREATE, 'Творческий'),
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICE, default=0)
    date = models.DateTimeField(auto_now=False)
    like = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return "Мероприятие: " + self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
