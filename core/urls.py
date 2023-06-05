from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from .views_admin import *

urlpatterns = [

    # # contato
    # path('create-contact/', create_contact),

    # # user
    path('user/create', create_user),
    # path('update-user/', update_user),
    path('auth/', CustomAuthToken.as_view()),
    path('user/', UserViewSetMixin.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>/', UserViewSetMixin.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

]
