# Generated by Django 4.2.1 on 2023-07-12 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardgame', '0003_alter_boardgame_publication_year'),
        ('rent', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentboardgame',
            name='boardgame_numbers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgame.boardgamenumbers'),
        ),
    ]