from rest_framework import serializers


def validate_username(value):
    if 'me' == value:
        raise serializers.ValidationError(
            "Вы не можете создать пользователя с именем me"
        )
    return value