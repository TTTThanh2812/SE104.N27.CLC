# Generated by Django 4.2.1 on 2023-07-10 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boardgame', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentBoardgame',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rental_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('deposit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('penalty_price', models.DecimalField(decimal_places=2, default='0', max_digits=8)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('rental_status', models.CharField(blank=True, choices=[('active', 'Active'), ('replied', 'Replied'), ('expired', 'Expired')], max_length=20)),
                ('boardgame_numbers', models.ForeignKey(limit_choices_to={'boardgame_number_status': 'in_stock'}, on_delete=django.db.models.deletion.CASCADE, to='boardgame.boardgamenumbers')),
            ],
            options={
                'ordering': ['rid'],
            },
        ),
    ]
