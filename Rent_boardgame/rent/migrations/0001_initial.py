# Generated by Django 4.2.1 on 2023-06-30 01:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boardgame', '0003_alter_boardgamereviews_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentBoardgame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rental_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('rental_status', models.CharField(blank=True, choices=[('active', 'Active'), ('replied', 'Replied'), ('expired', 'Expired')], max_length=20)),
                ('boardgame_numbers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.boardgamenumbers')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
