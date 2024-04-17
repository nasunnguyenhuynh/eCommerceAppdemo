from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, StatusConfirmationShop
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    def create(self, validated_data):  # hash password be4 store in database
        data = validated_data.copy()
        user = User(**data)  # unpacking dict and pass them as arg into init model User
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'avatar', 'first_name', 'last_name', 'email', 'birthday', 'phone']
        # 'is_staff', 'is_vendor', 'is_superuser', 'is_active'] Dont need to return, to affect to create a user with no oauth
        extra_kwargs = {  # prevent the password field returned when creating a new user
            'password': {
                'write_only': 'true'
            }
        }

    def to_representation(self, instance):  # ghi đè 1 trường trong fields
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url if instance.avatar and hasattr(instance.avatar, 'url') else None
        return rep


class ShopSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Shop
        fields = "__all__"


class StatusConfirmationShop(ModelSerializer):
    class Meta:
        model = StatusConfirmationShop
        fields = '__all__'


class ConfirmationShopSerializer(ModelSerializer):
    user = UserSerializer()
    status = StatusConfirmationShop()  # nếu ko serializer những khóa ngoại vẫn đc , nhưng ko ra đầy đủ thông tin

    class Meta:
        model = ConfirmationShop
        fields = ['id', 'user', 'status', 'citizen_identification_image']

    def to_representation(self, instance):  # ghi đè 1 trường trong fields
        rep = super().to_representation(instance)
        rep['citizen_identification_image'] = instance.citizen_identification_image.url

        return rep


class SendOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class VerifyOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
