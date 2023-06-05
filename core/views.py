from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins, viewsets
import json
import urllib
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import permissions
from .models import *
from .serializer import *

# pylint: disable=E1101
# pylint: disable=W0621


class CustomAuthToken(ObtainAuthToken):
    """ Class to create a custom token """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_active is True:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key
            })
        else:

            return Response({"message": "User is disabled!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """_summary_

    Returns:
        _type_: _description_
    """

    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()  # Replace `User` with your actual User model
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]