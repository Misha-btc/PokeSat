from django.views.generic import (
    ListView,
)

from .models import Sat, Transaction



def update_sat_based_on_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    sat = transaction.sat

    # Вызов метода для обновления Sat на основе Transaction
    sat.update_from_transaction(transaction)

class SatListView(ListView):
    model = Sat
    template_name = 'sat_list/index.html'
    context_object_name = 'sats'  # Название переменной контекста в шаблоне

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')  # Получение параметра сортировки из запроса
        queryset = super().get_queryset().order_by('-market_cap')  # Сначала отсортировать по капитализации

        for index, sat in enumerate(queryset, start=1):  # Присваиваем порядковые номера
            sat.rank = index
            sat.save(update_fields=['rank'])
        # Проверка наличия параметра сортировки и применение сортировки к QuerySet
        if order_by:
            if order_by == 'satribute':
                queryset = queryset.order_by('-satribute')
            elif order_by == '-satribute':
                queryset = queryset.order_by('satribute')
            elif order_by == 'rank':
                queryset = queryset.order_by('-rank')
            elif order_by == '-rank':
                queryset = queryset.order_by('rank')
            elif order_by == 'price':
                queryset = queryset.order_by('-price')
            elif order_by == '-price':
                queryset = queryset.order_by('price')
            elif order_by == 'market_cap':
                queryset = queryset.order_by('-market_cap')
            elif order_by == '-market_cap':
                queryset = queryset.order_by('market_cap')
            elif order_by == 'total_supply':
                queryset = queryset.order_by('-total_supply')
            elif order_by == '-total_supply':
                queryset = queryset.order_by('total_supply')
            elif order_by == 'circ_supply':
                queryset = queryset.order_by('-circ_supply')
            elif order_by == '-circ_supply':
                queryset = queryset.order_by('circ_supply')
            # Добавьте другие критерии сортировки по необходимости

        return queryset
