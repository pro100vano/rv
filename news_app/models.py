from django.db import models


class NewsModel(models.Model):
    title = models.CharField("Заголовок", max_length=150)
    text = models.TextField("Текст новости")
    image = models.ImageField("Изображение")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
