from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets, permissions
from .serializers import CardSerializer
from payments.models import Card, User
from rest_framework.response import Response
from rest_framework import status
import random
import string

def card_number_generator():
    digit = string.digits
    card_number = ''.join(random.choice(digit) for _ in range(16))
    return card_number


class CardsViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,):
    
    serializer_class = CardSerializer

    def get_data(self, request):
        data = {
            'card_number': card_number_generator(),
        }
        return data

    def get_queryset(self):
        return self.request.user.cards.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_data(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    

