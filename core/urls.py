"""
Module-level docstring providing a brief description of the module.
"""
from django.urls import path
from .views import CustomAuthToken, UserViewSetMixin, AnimalViewSetMixin


urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    path('user/', UserViewSetMixin.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>/', UserViewSetMixin.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('animal/', AnimalViewSetMixin.as_view(
        {'get': 'list', 'post': 'create'})),
    path('animal/<int:pk>/', AnimalViewSetMixin.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
