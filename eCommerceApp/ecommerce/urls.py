from django.urls import path, re_path, include
from django.shortcuts import redirect
from rest_framework import routers
from . import views

r = routers.DefaultRouter()

# api
# r.register('confirmationshop', views.ConfirmationShop)
r.register('users', views.UserViewSet)
r.register('categories', views.CategoryViewset, basename='categories')
# r.register('shops', views.ShopViewSet, basename='shops')
# r.register('login', views.LoginWithPasswordViewSet, basename='login-with-password')

urlpatterns = [
    path('', include(r.urls)),  # tạo api

    # nasun
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/login-with-sms/', views.login_with_sms, name='login_with_sms'),
    # Still not handle enter wrong OTP, expired OTP, Resend
    path('accounts/signup/', views.user_signup, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/basic-setup-profile/', views.basic_setup_profile, name='basic_setup_profile'),
    path('accounts/logout/', views.log_out, name='logout'),
    path('accounts/verify-otp/', views.verify_otp, name='verify_otp'),

    # controller
]
