from rest_framework import serializers
from payments.models import Card


class CardSerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Card
        fields = ('id', 'owner', 'card_number', 'balance')
