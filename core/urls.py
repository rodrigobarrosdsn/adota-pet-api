"""
Module-level docstring providing a brief description of the module.
"""
from django.contrib import admin
from django.urls import include, path
from .views import CustomAuthToken, UserViewSetMixin, AnimalViewSetMixin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Adota Pet API",
        default_version='v1',
        description="API para adoção de animais",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@adotapet.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    path('user/', UserViewSetMixin.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>/', UserViewSetMixin.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('animal/', AnimalViewSetMixin.as_view(
        {'get': 'list', 'post': 'create'})),
    path('animal/<int:pk>/', AnimalViewSetMixin.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('user/animals/', AnimalViewSetMixin.as_view({'get': 'user_animal'}), name='user_animal'),

]

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa E501
]
