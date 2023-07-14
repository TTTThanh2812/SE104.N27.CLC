# Generated by Django 4.2.1 on 2023-07-13 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boardgame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardgamereviews',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='boardgamenumbers',
            name='boardgame',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boardgame_numbers', to='boardgame.boardgame'),
        ),
        migrations.AddField(
            model_name='boardgameimages',
            name='boardgame',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='boardgame.boardgame'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='boardgame.author'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='boardgame.category'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='boardgame.producer'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='boardgame.version'),
        ),
    ]
