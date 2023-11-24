from django.core.management.base import BaseCommand
from sat_list.models import Bitcoin

import requests


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '0d84af23-7fe7-4417-b09a-12832f235060',
        }
        response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank', headers=headers)  # URL вашего API
        data = response.json()
        bitcoin_price = data['data'][0]['quote']['USD']['price']
        print(f"Цена Биткоина: {bitcoin_price}")
        bitcoin, created = Bitcoin.objects.update_or_create(
            # Параметры для идентификации объекта, например:
            name="Bitcoin",
            defaults={
                'price': bitcoin_price,
            }
        )

