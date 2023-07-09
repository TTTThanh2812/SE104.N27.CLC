# Generated by Django 4.2.1 on 2023-07-08 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardgame', '0004_alter_boardgamenumbers_boardgame_number_status'),
        ('rent', '0002_alter_rentboardgame_deposit_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentboardgame',
            name='boardgame_numbers',
            field=models.ForeignKey(limit_choices_to={'boardgame_number_status': 'in_stock'}, on_delete=django.db.models.deletion.CASCADE, to='boardgame.boardgamenumbers'),
        ),
    ]
