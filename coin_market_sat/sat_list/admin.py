from django.contrib import admin
from .models import Sat

admin.site.empty_value_display = 'Не задано'

class SatInline(admin.TabularInline):
    model = Sat
    extra = 0


@admin.register(Sat)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'satribute',
    )
    search_fields = ('satribute',)
    list_filter = ('market_cap',)
    list_display_links = ('satribute',)