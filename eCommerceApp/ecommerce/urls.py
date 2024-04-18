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
    path('accounts/login-with-sms/', views.send_otp, name='login-with-sms'),
    # Still not handle enter wrong OTP, expired OTP, Resend
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/logout/', views.log_out, name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # controller
]
