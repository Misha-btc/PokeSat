# Generated by Django 3.2.16 on 2023-11-16 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sat_list', '0002_sat_order_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sat',
            options={'default_related_name': 'Sats', 'ordering': ('-market_cap',), 'verbose_name': 'Sat', 'verbose_name_plural': 'Sats'},
        ),
    ]