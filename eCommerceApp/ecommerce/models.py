from enum import unique

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


# class CustomUserManager(BaseUserManager):
#     def create_superuser(self, email, password=None, **extra_fields):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         :param email:
#         :param password:
#         :param **extra_fields:
#         """
#
#         user_details = UserDetails(firstname='admin', lastname='admin', birthday=datetime.now())
#         user_details.save(using=self._db)
#
#         user = self.create_user(
#             email,
#             password=password,
#             user_details=user_details,
#             **extra_fields)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#

class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    is_vendor = models.BooleanField(default=False)
    birthday = models.DateTimeField(null=True)
    phone = models.CharField(max_length=10, null=False, unique=True)

    # objects = CustomUserManager()


class UserAddresses(models.Model):
    address = models.CharField(max_length=100, null=False)
    user_details = models.ForeignKey(User, on_delete=models.CASCADE)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    img = CloudinaryField(null=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Shop(BaseModel):
    name = models.CharField(max_length=100)
    following = models.IntegerField(default=0)
    followed = models.IntegerField(default=0)
    rating = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Product(BaseModel):
    name = models.CharField(max_length=150)
    price = models.FloatField(null=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, default=None)


class ProductImageDetail(models.Model):
    image = CloudinaryField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)


class ProductImagesColors(models.Model):
    name_color = models.CharField(max_length=50)
    url_image = CloudinaryField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)


def validate_video_size(value):
    max_size = 30 * 1024 * 1024  # 50MB
    if value.size > max_size:
        raise ValidationError("Video size should not exceed 30MB.")


class ProductVideos(models.Model):
    url_video = CloudinaryField(resource_type='video', allowed_formats=['mp4', 'webm'],
                                validators=[validate_video_size])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)


class ProductInfo(models.Model):
    origin = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    description = RichTextField(null=True)
    manufacture = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)


class ProductSell(models.Model):
    sold_quantity = models.IntegerField(null=False)
    insurrance = models.DateTimeField(null=True, default=None)
    percent_sale = models.IntegerField()
    rating = models.FloatField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=30)
    fee = models.FloatField()


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30)


class Condition(models.Model):
    order_fee_min = models.FloatField()
    voucher_sale_max = models.FloatField()
    time_usable = models.DateTimeField()
    time_expired = models.DateTimeField()


class VoucherType(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    key = models.CharField(max_length=10, unique=True, null=False)


class Voucher(BaseModel):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10, unique=True, null=False)
    description = RichTextField()
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)


class Order(models.Model):
    transportation = models.ForeignKey(ShippingMethod, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(null=False)


class Orders_Products(models.Model):
    quantity = models.IntegerField(null=False)
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Orders_Vouchers(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT)


class CommentAndRating(models.Model):
    content = RichTextField()
    ratedShop = models.FloatField()
    ratedProduct = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
