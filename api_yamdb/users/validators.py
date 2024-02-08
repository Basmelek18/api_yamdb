from rest_framework import serializers


def validate_username(value):
    if 'me' == value:
        raise serializers.ValidationError(
            "You can't create a user named me"
        )
    return value
