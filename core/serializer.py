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
    old_password = serializers.CharField(write_only=True, required=False)

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
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            import ipdb
            ipdb.set_trace()
            raise serializers.ValidationError({'detail': 'Senha inválida'})

        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update password if provided
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id',)
