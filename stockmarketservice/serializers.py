import logging
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class SignupSerializer(serializers.HyperlinkedModelSerializer):

    first_name  = serializers.CharField(required=True, label="Name", validators=[MinLengthValidator(3, 'The field must contain at least 3 characters')])
    last_name   = serializers.CharField(required=True, label="Last Name", validators=[MinLengthValidator(3, 'The field must contain at least 3 characters')])
    email       = serializers.EmailField(required=True, style={'input_type': 'email'}, validators=[UniqueValidator(queryset=User.objects.all())])
    password    = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}, validators=[MinLengthValidator(8, 'The field must contain at least 8 characters')])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(email       = validated_data['email'],
                                        username    = validated_data['email'],
                                        password    = validated_data['password'],
                                        first_name  = validated_data['first_name'],
                                        last_name   = validated_data['last_name'])
        return user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

class DailyPricesSerializer(serializers.HyperlinkedModelSerializer):
    openPrice       = serializers.CharField(max_length=255)
    higherPrice     = serializers.CharField(max_length=255)
    lowerPrice      = serializers.CharField(max_length=255)
    closeVariation  = serializers.CharField(max_length=255)