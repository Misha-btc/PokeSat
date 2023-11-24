from .models import Bitcoin

def bitcoin_price(request):
    bitcoin = Bitcoin.objects.first()
    return {'bitcoin_price': bitcoin.price if bitcoin else None}