# Generated by Django 4.2.1 on 2023-07-22 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_rentboardgame_deposit_refund_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentboardgame',
            name='description',
            field=models.TextField(blank=True, default='This is notes on orders', null=True),
        ),
    ]
