from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()

urlpatterns = [
    path('', include(r.urls)),  # tạo api
    path('display/', views.display, name='display'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),

]
