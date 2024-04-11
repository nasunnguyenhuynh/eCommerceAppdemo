from django.template import loader
from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, StatusConfirmationShop
from rest_framework import viewsets, generics, status, parsers
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response


def display(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


######################################################
import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('sign_in')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')


#################################

#
# from .models import User, Place, Purpose, Meeting, GuestMeeting
#
#
#
# class PlaceViewset(viewsets.ViewSet, generics.ListAPIView):
#     queryset = Place.objects.all()
#     serializer_class = serializers.PlaceSerializer


########################################### View của darklord0710 ######################################################

class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(methods=['get'], url_path='confirmationShop', detail=True)
    def getConfirmatonShop(self, request, pk):
        confirmationShops = self.get_object().confirmationshop_set.select_related('user')  # qh 1-1 mới nên join
        return Response(serializers.ConfirmationShopSerializer(confirmationShops, many=True).data,
                        status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    pass


class ConfirmationShop(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = ConfirmationShop.objects.all()
    serializer_class = serializers.ConfirmationShopSerializer
