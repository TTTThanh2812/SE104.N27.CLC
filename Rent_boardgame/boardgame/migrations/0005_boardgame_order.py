# Generated by Django 4.2.1 on 2023-07-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardgame', '0004_alter_boardgamenumbers_boardgame_number_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardgame',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
