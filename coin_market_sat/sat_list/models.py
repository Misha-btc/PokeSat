from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class Bitcoin(models.Model):
    name = models.CharField('Satribute', max_length=50, default='Bitcoin')
    price = models.FloatField('Bitcoin price:', default=37000)


class Sat(models.Model):
    satribute = models.CharField('Satribute', max_length=50)
    price = models.FloatField('Floor Price', default=0)
    market_cap = models.IntegerField('Market Cap', default=0)
    total_supply = models.IntegerField('Total Supply', default=0)
    circ_supply = models.IntegerField('Circulating Supply', default=0)
    rank = models.IntegerField(null=True, blank=True)

    def update_from_transaction(self, new_price, total_satribute):
        # Обновите атрибуты объекта Sat
        self.price = new_price
        bitcoin = Bitcoin.objects.first()
        bitcoin_price = bitcoin.price if bitcoin else 0
        self.market_cap = self.price * self.circ_supply  -  total_satribute / 100000000 * bitcoin_price
        # Вы можете выполнить другие арифметические операции и обновить другие атрибуты Sat
        # Сохраните изменения в базе данных
        self.save()

    class Meta:
        verbose_name = 'Sat'
        verbose_name_plural = 'Sats'
        default_related_name = 'Sats'
        ordering = ('-market_cap',)

    def __str__(self):
        return self.satribute
    
class Transaction(models.Model):
    satribute = models.CharField(max_length=100)
    new_owner = models.CharField(max_length=100)
    listed_price = models.FloatField(default=0)
    satribute_amount = models.FloatField(default=0)
    date = models.DateTimeField()
    tokenid = models.CharField(max_length=200)
    sat = models.ForeignKey(
        Sat,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Sat',
    )

@receiver(post_save, sender=Transaction)
def update_sat(sender, instance, **kwargs):
    # Текущее время в UTC
    now_utc = timezone.now()

    # Вычисляем время два часа назад в UTC
    two_hours_ago_utc = now_utc - timedelta(hours=2)

    # Фильтруем транзакции за последние два часа в UTC
    recent_transactions = Transaction.objects.filter(
        satribute=instance.satribute, 
        date__gte=two_hours_ago_utc
    )
    total_price = sum(t.listed_price for t in recent_transactions)
    total_satribute = sum(t.satribute_amount for t in recent_transactions)
    bitcoin = Bitcoin.objects.first()
    bitcoin_price = bitcoin.price if bitcoin else 0
    avg_price = total_price / total_satribute  / 100000000 * bitcoin_price
    sat = instance.sat
        # Вызов метода для обновления Sat на основе Transaction
    sat.update_from_transaction(avg_price, total_satribute)
