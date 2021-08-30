from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
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
    balance = models.IntegerField(
        'Баланс карты',
        default=0,
    )
    creation_date = models.DateTimeField(
        'Дата создания карты',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f'{self.owner}-{self.card_number}-{self.balance}'
