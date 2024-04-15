from django.shortcuts import render
from django.contrib.auth import logout
from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, \
    StatusConfirmationShop
from rest_framework import viewsets, generics, status, parsers, permissions
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

# =========== Start Oauth2 ===============

import re
from django.contrib import messages
from django.http import HttpResponseRedirect


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def profile_view(request):
    # Get image from SocialAccount
    # if request.user.is_authenticated:
    #     extra_data = SocialAccount.objects.get(user=request.user).extra_data
    #     print(extra_data['picture'])
    # else:
    #     print("User not authenticated")
    if request.user.is_authenticated:
        return render(request, 'noti.html')


def log_out(request):
    logout(request)
    return render(request, 'login.html')


# =========== End Oauth2 ===============

#
# from .models import User, Place, Purpose, Meeting, GuestMeeting
#
#
#
# class PlaceViewset(viewsets.ViewSet, generics.ListAPIView):
#     queryset = Place.objects.all()
#     serializer_class = serializers.PlaceSerializer


########################################### View của darklord0710 ######################################################

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['get_current_user', 'get_post_patch_confirmationshop', 'get_shop']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny(), ]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):  # PATCH này phải viết hoa
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)

    @action(methods=['post'], url_path='user', detail=False)
    def post_current_user(self, request):
        avatar = request.data.get('avatar')
        phone = request.data.get('phone')
        birthday = request.data.get('birthday')
        password = request.data.get('password')
        # user = self.get_object().create()

    @action(methods=['get', 'post', 'patch'], url_path='confirmationshop', detail=True)
    def get_post_patch_confirmationshop(self, request, pk):
        if request.method.__eq__('PATCH'):  # Patch vẫn cập nhật đc 2 dòng ảnh và status
            citizen_identification_image_data = request.data.get('citizen_identification_image')
            # confirmationShops = self.get_object().confirmationshop_set.get(user=request.user.id)
            confirmationShops = ConfirmationShop.objects.get(user_id=pk)
            confirmationShops.citizen_identification_image = citizen_identification_image_data
            confirmationShops.status = StatusConfirmationShop.objects.get(
                id=4)  # chỗ này phải sửa cả object , ko thể sửa mỗi id khóa ngoại
            confirmationShops.save()
            return Response(serializers.ConfirmationShopSerializer(confirmationShops).data,
                            status=status.HTTP_200_OK)  # nếu gắn many=True ở đây sẽ bị lỗi not iterable

        elif request.method.__eq__('POST'):
            citizen_identification_image_data = request.data.get('citizen_identification_image')
            status_confirm_shop = StatusConfirmationShop.objects.get(id=4)
            c = self.get_object().confirmationshop_set.create(user=request.user, status=status_confirm_shop,
                                                              citizen_identification_image=citizen_identification_image_data)

            return Response(serializers.ConfirmationShopSerializer(c).data, status=status.HTTP_201_CREATED)

        # confirmationShops = ConfirmationShop.objects.get(user_id=pk)
        confirmationShops = self.get_object().confirmationshop_set.select_related(
            'user')  # chỉ join khi có quan hệ 1-1 # .all() hay không có đều đc ????
        return Response(serializers.ConfirmationShopSerializer(confirmationShops, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], url_path="shop", detail=True)
    def get_shop(self, request, pk):
        shop = self.get_object().shop_set.filter(active=True, user_id=pk).first()
        # shop = Shop.objects.get(active=True, user_id=pk)
        return Response(serializers.ShopSerializer(shop).data, status=status.HTTP_200_OK)

    parser_classes = [
        parsers.MultiPartParser, ]


class ShopViewSet(viewsets.ViewSet, generics.CreateAPIView):
    serializers_class = serializers.ShopSerializer


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    pass
