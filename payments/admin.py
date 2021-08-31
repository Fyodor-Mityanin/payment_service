from django.contrib import admin

from .models import Card, User2CardTransaction, Invoice, Card2CardTransaction


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'owner',
        'card_number',
        'balance',
        'creation_date',
    )


class User2CardTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'card',
        'amount',
        'transaction_date',
    )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'sellers_card',
        'buyer',
        'amount',
        'invoice_date',
        'is_paid',
    )

class Card2CardTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'incoming_card',
        'outgoing_card',
        'amount',
        'transaction_date',
    )


admin.site.register(Card, CardAdmin)
admin.site.register(User2CardTransaction, User2CardTransactionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Card2CardTransaction, Card2CardTransactionAdmin)
