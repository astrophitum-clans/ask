# Generated by Django 4.2.1 on 2023-06-05 15:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='answer_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='unlikes',
            field=models.ManyToManyField(related_name='answer_unlikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='question_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='unlikes',
            field=models.ManyToManyField(related_name='question_unlikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
