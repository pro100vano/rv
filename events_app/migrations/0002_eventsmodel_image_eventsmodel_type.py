# Generated by Django 4.0.4 on 2022-05-22 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='eventsmodel',
            name='type',
            field=models.IntegerField(choices=[(0, 'Спортивнй'), (1, 'Развлекательный'), (2, 'Лечебный'), (3, 'Творческий')], default=0),
        ),
    ]
