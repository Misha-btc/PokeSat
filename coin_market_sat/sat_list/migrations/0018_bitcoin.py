# Generated by Django 3.2.16 on 2023-11-23 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sat_list', '0017_transaction_tokenid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitcoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=37000, verbose_name='Bitcoin price:')),
            ],
        ),
    ]