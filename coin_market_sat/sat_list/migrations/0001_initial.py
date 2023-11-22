# Generated by Django 3.2.16 on 2023-11-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satribute', models.CharField(max_length=50, verbose_name='Satribute')),
                ('price', models.FloatField(default=0, verbose_name='Floor Price')),
                ('market_cap', models.IntegerField(default=0, verbose_name='Market Cap')),
                ('total_supply', models.IntegerField(default=0, verbose_name='Total Supply')),
                ('circ_supply', models.IntegerField(default=0, verbose_name='Circulating Supply')),
            ],
            options={
                'verbose_name': 'Sat',
                'verbose_name_plural': 'Sats',
                'ordering': ('satribute',),
                'default_related_name': 'Sats',
            },
        ),
    ]
