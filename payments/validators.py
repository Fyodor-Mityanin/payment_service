from django.core.exceptions import ValidationError


def validate_card_is_digit(value):
    if not (value.isdigit() and len(value) == 16):
        raise ValidationError(
            '%(value)s must be 16 digits', params={'value': value},
        )
