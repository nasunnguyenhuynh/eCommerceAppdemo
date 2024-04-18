from allauth.socialaccount.models import SocialAccount
import cloudinary.uploader, random
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, \
    StatusConfirmationShop
from rest_framework import viewsets, generics, status, parsers, permissions
from . import serializers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.core.cache import cache
# from twilio.rest import Client
from .serializers import SendOTPRequestSerializer, VerifyOTPRequestSerializer


# =========== Start Oauth2 ===============
# in adpater.py
# def get_app(self, request, provider, client_id=None):
#     from allauth.socialaccount.models import SocialApp
#
#     apps = self.list_apps(request, provider=provider, client_id=client_id)
#     if len(apps) > 1:
#         # raise MultipleObjectsReturned
#         pass
#     elif len(apps) == 0:
#         raise SocialApp.DoesNotExist()
#     return apps[0]


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def profile_view(request):
    picture_url = None
    if request.user.is_authenticated:
        user = request.user
        if not user.avatar:
            try:
                social_account = SocialAccount.objects.get(user=user)
                extra_data = social_account.extra_data
                picture_url = extra_data.get('picture')
                if picture_url:
                    # Tải hình ảnh từ URL và lưu vào CloudinaryField
                    upload_result = cloudinary.uploader.upload(picture_url)
                    user.avatar = upload_result['url']
                    user.save()
                    print(f"URL mới được lưu trong Cloudinary: {user.avatar}")
            except SocialAccount.DoesNotExist:
                print("Không có thông tin SocialAccount tương ứng.")
        else:
            print(f"Hình ảnh hiện tại từ Cloudinary: {user.avatar.url}")
            picture_url = user.avatar.url
            return render(request, 'noti.html', {'picture_url': picture_url})
    else:
        print("User not authenticated")
    return render(request, 'noti.html', {'picture_url': picture_url})


def log_out(request):
    logout(request)
    return render(request, 'login.html')


# =========== End Oauth2 ===============
# =========== Start OTP ===============
# Test Postman
# POST /verify-otp/ phone_number, otp
# POST /login-with-sms/ phone_number
# Thời gian hết hạn của mã OTP (đơn vị: giây)
OTP_EXPIRY_SECONDS = 300  # 5 phút


def generate_otp():
    return str(random.randint(100000, 999999))


@api_view(['GET', 'POST'])
def send_otp(request):
    if request.method == 'GET':
        return render(request, 'loginWithSms.html')

    if request.method == 'POST':
        serializer = SendOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Tạo mã OTP ngẫu nhiên
            otp = generate_otp()
            print(otp)
            # Lưu mã OTP vào cache với khóa là số điện thoại
            cache.set(phone_number, otp, timeout=OTP_EXPIRY_SECONDS)
            print(phone_number)
            # Gửi mã OTP đến số điện thoại bằng Twilio
            # account_sid = 'ACf3bd63d2afda19fdcb1a7ab22793a8b8'
            # auth_token = '[AuthToken]'
            # client = Client(account_sid, auth_token)
            # message_body = f'DJANGO: Nhập mã xác minh {otp} để đăng ký tài khoản. Mã có hiệu lực trong 5 phút.'
            # message = client.messages.create(
            #     from_='+12513090557',
            #     body=message_body,
            #     to=phone_number
            # )
            return render(request, 'verifyOTP.html', {'phone_number': phone_number})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        # Lấy mã OTP từ cache
        cached_otp = cache.get(phone_number)

        # Kiểm tra xem mã OTP đã hết hạn chưa
        if cached_otp is None:
            return Response({'message': 'Mã OTP đã hết hạn.'}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem mã OTP nhập vào có khớp với mã OTP trong cache hay không
        if otp == cached_otp:
            # Xóa mã OTP từ cache sau khi đã sử dụng
            cache.delete(phone_number)
            return redirect('/')
        else:
            return Response({'message': 'Mã OTP không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========== End OTP ===============


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
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user', 'get_post_patch_confirmationshop', 'get_shop']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny(), ]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)  # /users/current-user/
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):  # PATCH này phải viết hoa
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)

    @action(methods=['post'], url_path='user', detail=False)  # /users/user/
    def post_current_user(self, request):
        avatar = request.data.get('avatar')
        phone = request.data.get('phone')
        birthday = request.data.get('birthday')
        password = request.data.get('password')
        # user = self.get_object().create()

    @action(methods=['get', 'post', 'patch'], url_path='confirmationshop', detail=True)  # /users/{id}/confirmationshop/
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

    @action(methods=['get'], url_path="shop", detail=True)  # /users/{id}/shop/
    def get_shop(self, request, pk):
        shop = self.get_object().shop_set.filter(active=True, user_id=pk).first()
        # shop = Shop.objects.get(active=True, user_id=pk)
        return Response(serializers.ShopSerializer(shop).data, status=status.HTTP_200_OK)


class ShopViewSet(viewsets.ViewSet, generics.CreateAPIView):
    serializers_class = serializers.ShopSerializer


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    pass
