import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from . import models
from .constants import CONTACT_NUMBER_REGEX


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=models.User.objects.all(), message="This email already exits",
    )])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)

    token_key = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name', 'contact_number', 'password', 'confirm_password',
                  'email', 'token_key')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'last_name': {'required': True, 'allow_null': False, 'allow_blank': False},
            'contact_number': {'required': True, 'allow_null': False, 'allow_blank': False,
                               'min_length': 10, 'max_length': 15}
        }

    def validate_contact_number(self, value):
        if not re.match(CONTACT_NUMBER_REGEX, value):
            raise serializers.ValidationError("Invalid phone number")

        return value

    def get_token_key(self, instance):
        if self.instance:
            token, created = Token.objects.get_or_create(user=instance)
            return token.key
        return None

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password', None)
        password = attrs.get('password', None)
        if not password == confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Password not matched'})
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user
