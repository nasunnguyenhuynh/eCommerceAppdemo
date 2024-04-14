from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, StatusConfirmationShop
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'first_name', 'last_name', 'email', 'birthday', 'phone', 'is_staff',
                  'is_vendor', 'is_superuser', 'is_active']

    def to_representation(self, instance):  # ghi đè 1 trường trong fields
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

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
