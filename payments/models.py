from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import validate_card_is_digit

User = get_user_model()


class Card(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Владелец',
    )
    card_number = models.CharField(
        'Номер карты',
        unique=True,
        max_length=16,
        validators=[
            validate_card_is_digit,
            MinLengthValidator(
                16,
                'Номер карты должен содержать 16 цифр'
            ),
        ]
    )
    balance = models.DecimalField(
        'Баланс карты',
        default=0,
        max_digits=8,
        decimal_places=2
    )
    creation_date = models.DateTimeField(
        'Дата создания карты',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        balance = self.round_balance()
        return f'{self.card_number}'

    def round_balance(self):
        return round(self.balance, 2)


class User2CardTransaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user2card_transactions',
        verbose_name='Отправитель',
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='user2card_transactions',
        verbose_name='Карта получения',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=8,
        decimal_places=2
    )
    transaction_date = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = 'User2Card транзакция'
        verbose_name_plural = 'User2Card транзакции'

    def __str__(self):
        return f'{self.user}->{self.card} : {self.amount}'


class Invoice(models.Model):
    sellers_card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='sent_invoices',
        verbose_name='Счёт оплаты',
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_invoices',
        verbose_name='Покупатель',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=8,
        decimal_places=2
    )
    invoice_date = models.DateTimeField(
        'Дата и время получения инвойса',
        auto_now_add=True,
    )
    is_paid = models.BooleanField(
        'Оплачено?',
        default=False
    )

    class Meta:
        ordering = ['-invoice_date']
        verbose_name = 'Инвойс'
        verbose_name_plural = 'Инвойсы'

    def __str__(self):
        return f'{self.sellers_card}->{self.buyer}:{self.amount}'


class Card2CardTransaction(models.Model):
    incoming_card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='card2card_incoming_transactions',
        verbose_name='Карта получения денег',
    )
    outgoing_card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='card2card_outgoing_transactions',
        verbose_name='Карта отправления денег',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=8,
        decimal_places=2
    )
    email = models.EmailField(
        'Почта',
        blank=True,
        null=True,
    )
    transaction_date = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = 'Card2Card транзакция'
        verbose_name_plural = 'Card2Card транзакции'

    def __str__(self):
        return f'{self.outgoing_card}->{self.incoming_card} : {self.amount}'
