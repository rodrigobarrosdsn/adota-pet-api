"""_summary_"""
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Animal, User
from .serializer import AnimalSerializer, UserSerializer
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


class UserFilter(filters.FilterSet):
    """
    _summary_
    """
    email = filters.CharFilter(field_name='email', lookup_expr='exact')
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')

    class Meta:
        """_summary_
        """
        model = User
        fields = ['email', 'nome', 'is_active']


class UserViewSetMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """_summary_"""
    queryset = User.objects.all()  # Replace `User` with your actual User model
    serializer_class = UserSerializer
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = UserFilter

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class AnimalFilter(filters.FilterSet):
    """Animal Filter Class"""
    apelido = filters.CharFilter(field_name='apelido', lookup_expr='icontains')
    idade = filters.CharFilter(field_name='idade', lookup_expr='icontains')
    porte = filters.CharFilter(field_name='porte', lookup_expr='icontains')
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')

    class Meta:
        """
        _summary_
        """
        model = Animal
        fields = ['apelido', 'idade', 'porte', 'nome', 'is_active']


class AnimalViewSetMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """_summary_
    """
    queryset = Animal.objects.all()  # Replace `Animal` with your actual Animal model
    serializer_class = AnimalSerializer
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = AnimalFilter

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
