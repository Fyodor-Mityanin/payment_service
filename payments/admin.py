from django.contrib import admin

from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'owner',
        'card_number',
        'balance',
    )
    search_fields = ('owner',)


admin.site.register(Card, CardAdmin)
