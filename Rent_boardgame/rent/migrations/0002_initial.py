# Generated by Django 4.2.1 on 2023-07-21 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boardgame', '0002_initial'),
        ('rent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentboardgame',
            name='renter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='boardgame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.boardgame'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
