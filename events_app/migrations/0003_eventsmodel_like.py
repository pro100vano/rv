# Generated by Django 4.0.4 on 2022-05-22 04:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events_app', '0002_eventsmodel_image_eventsmodel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsmodel',
            name='like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
