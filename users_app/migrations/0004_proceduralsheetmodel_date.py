# Generated by Django 4.0.4 on 2022-05-22 02:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0003_proceduralsheetmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='proceduralsheetmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
