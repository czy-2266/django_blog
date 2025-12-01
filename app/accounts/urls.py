from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/', views.login, name='token'),
    path('users/me/', views.user_detail, name='user-detail'),
]