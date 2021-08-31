from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from payments.models import Card, Invoice


class IsOwner(permissions.BasePermission):
    message = 'You must be the owner of this object.'

    def has_permission(self, request, view):
        card = get_object_or_404(Card, id=view.kwargs.get('pk'))
        return card.owner == request.user

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsBuyer(permissions.BasePermission):
    message = 'You must be the buyer of this invoice.'

    def has_permission(self, request, view):
        invoice = get_object_or_404(Invoice, id=view.kwargs.get('pk'))
        return invoice.buyer == request.user

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
