# Generated by Django 3.2.16 on 2023-11-16 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sat_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sat',
            name='order_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
