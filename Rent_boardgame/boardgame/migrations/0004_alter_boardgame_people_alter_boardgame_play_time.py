# Generated by Django 4.2.1 on 2023-07-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardgame', '0003_alter_boardgame_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='people',
            field=models.IntegerField(max_length=100),
        ),
        migrations.AlterField(
            model_name='boardgame',
            name='play_time',
            field=models.IntegerField(max_length=50),
        ),
    ]