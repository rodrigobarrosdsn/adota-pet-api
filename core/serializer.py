from dataclasses import field
from rest_framework import serializers
from .models import *
# from drf_base64.fields import Base64ImageField, Base64FileField
from django.db.models import Sum
from rest_framework.response import Response
from ast import literal_eval
import base64
from adotapet.settings import *
from django.core.files.base import ContentFile
from django.db.models import Q
from django.db.models import Avg, Sum, Count, Min, Max
import re
from rest_framework import viewsets, status
# from drf_base64.fields import Base64ImageField, Base64FileField


class UserSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    # profile_image = Base64ImageField(required=False)
    # profile_image_url = serializers.SerializerMethodField()

    # def get_profile_image_url(self, obj):
    #     if obj != None and obj.profile_image != None:
    #         return BASE_URL + MEDIA_URL + obj.profile_image.name
    #     return None

    def create(self, validated_data):
        """_summary_

        Args:
            validated_data (_type_): _description_

        Returns:
            _type_: _description_
        """
        password = validated_data.pop('password')

        validated_data['is_active'] = True

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """_summary_

        Args:
            instance (_type_): _description_
            validated_data (_type_): _description_

        Returns:
            _type_: _description_
        """
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            return Response({'detail': 'Senha inválida'}, status=status.HTTP_400_BAD_REQUEST)

        if password is not None:
            instance.set_password(password)

        new_instance = super().update(instance, validated_data)
        return new_instance

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id',)
