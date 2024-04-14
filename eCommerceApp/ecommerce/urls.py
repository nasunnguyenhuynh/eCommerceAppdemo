from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()

# api
r.register('users', views.UserViewSet)
# r.register('confirmationshop', views.ConfirmationShop)

urlpatterns = [
    path('', include(r.urls)),  # tạo api

    # nasun
    path('accounts/login/', views.display, name='display'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/logout/', views.log_out, name='logout'),

    # controller
]
