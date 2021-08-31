import random
import string
from decimal import Decimal

from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from payments.models import Card, Invoice

from .permissions import IsBuyer, IsOwner
from .serializers import (Card2CardTransactionSerializer, CardSerializer,
                          CustomUserSerializer, InvoiceSerializer,
                          User2CardTransactionSerializer)

ALREADY_PAID_RESPONSE = JsonResponse({'error': 'invoice already paid'})
TRANSACTION_ERROR_RESPONSE = JsonResponse(
    {'error': 'transaction error, please try again later'}
)
UNKNOWN_CARD_RESPONSE = JsonResponse({'error': 'Card number is unknown'})
EMAIL_HOST_USER = 'payment_service@example.com'


def send_invoice_has_paid_email(data):
    email_to = data.get('email')
    amount = data.get('amount')
    card_number = data.get('outgoing_card')
    text = f'You paid {amount} money from your card {card_number}'
    send_mail(
        'The bill is paid',
        text,
        EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )


class UserDetailAPI(views.APIView):
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


class CardListCreateAPI(views.APIView):
    def card_number_generator(self):
        digit = string.digits
        card_number = ''.join(random.choice(digit) for _ in range(16))
        return card_number

    def get_data(self, request):
        data = {'card_number': self.card_number_generator(), }
        return data

    def get(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=self.get_data(request))
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailDestroyAPI(views.APIView):
    permission_classes = [IsOwner, ]

    def get(self, request, pk):
        card = get_object_or_404(Card, id=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = get_object_or_404(Card, id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        serializer = User2CardTransactionSerializer(data=request.data)
        if serializer.is_valid():
            card = get_object_or_404(Card, id=pk)
            try:
                serializer.save(user=request.user, card=card)
                card.balance += Decimal(request.data.get('amount'))
                card.save()
            except Exception:
                return TRANSACTION_ERROR_RESPONSE
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceListCreateAPI(views.APIView):
    def get(self, request):
        invoice = request.user.received_invoices.filter(is_paid=False)
        serializer = InvoiceSerializer(invoice, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not Card.objects.filter(
            owner=request.user, card_number=request.data.get('sellers_card')
        ).exists():
            return UNKNOWN_CARD_RESPONSE
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailPayAPI(views.APIView):
    permission_classes = [IsBuyer, ]

    def card_2_card_transaction(self, invoice, data):
        outgoing_card = get_object_or_404(
            Card, card_number=data.get('outgoing_card')
        )
        invoice.sellers_card.balance += Decimal(data.get('amount'))
        invoice.sellers_card.save()
        outgoing_card.balance -= Decimal(data.get('amount'))
        outgoing_card.save()
        invoice.is_paid = True
        invoice.save()
        if data.get('email'):
            send_invoice_has_paid_email(data)

    def get_data(self, request, invoice):
        data = {
            'outgoing_card': request.data.get('outgoing_card'),
            'incoming_card': invoice.sellers_card.card_number,
            'amount': invoice.amount,
            'email': request.data.get('email'),
        }
        return data

    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, id=pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        if invoice.is_paid:
            return ALREADY_PAID_RESPONSE
        data = self.get_data(request, invoice)
        if not Card.objects.filter(
            owner=request.user, card_number=data.get('outgoing_card')
        ).exists():
            return UNKNOWN_CARD_RESPONSE
        serializer = Card2CardTransactionSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                self.card_2_card_transaction(invoice, data)
            except Exception:
                return TRANSACTION_ERROR_RESPONSE
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
