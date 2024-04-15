from django.urls import path, re_path, include
from django.shortcuts import redirect
from rest_framework import routers
from . import views

r = routers.DefaultRouter()

# api
r.register('users', views.UserViewSet)
# r.register('confirmationshop', views.ConfirmationShop)

urlpatterns = [
    path('', include(r.urls)),  # tạo api

    # nasun
    path('accounts/login/', views.login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/logout/', views.log_out, name='logout'),

    # controller
]
