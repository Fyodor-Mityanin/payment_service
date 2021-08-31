from djoser.serializers import UserSerializer
from rest_framework import serializers

from payments.models import (Card, Card2CardTransaction, Invoice, User,
                             User2CardTransaction)


class CardSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    user2card_transactions = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    card2card_incoming_transactions = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    card2card_outgoing_transactions = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Card
        fields = ('id', 'owner', 'card_number', 'balance',
                  'user2card_transactions', 'card2card_incoming_transactions',
                  'card2card_outgoing_transactions')


class User2CardTransactionSerializer(serializers.ModelSerializer):
    card = serializers.StringRelatedField(
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = User2CardTransaction
        fields = ('id', 'user', 'amount',  'card', 'transaction_date')


class InvoiceSerializer(serializers.ModelSerializer):
    sellers_card = serializers.SlugRelatedField(
        slug_field='card_number',
        queryset=Card.objects.all()
    )
    buyer = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Invoice
        fields = ('id', 'sellers_card', 'buyer',
                  'amount', 'invoice_date', 'is_paid',)


class Card2CardTransactionSerializer(serializers.ModelSerializer):
    incoming_card = serializers.SlugRelatedField(
        slug_field='card_number',
        queryset=Card.objects.all(),
    )
    outgoing_card = serializers.SlugRelatedField(
        slug_field='card_number',
        queryset=Card.objects.all(),
    )
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = Card2CardTransaction
        fields = ('id', 'incoming_card', 'outgoing_card',
                  'amount', 'transaction_date', 'email')


class CustomUserSerializer(UserSerializer):
    cards = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    user2card_transactions = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'cards', 'user2card_transactions')
