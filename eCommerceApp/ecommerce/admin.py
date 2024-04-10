from cloudinary.models import CloudinaryField
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin
from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'birthday', 'is_active', 'is_vendor',
                    'is_superuser',
                    'my_image']
    search_fields = ['id', 'username']
    list_filter = ['id', 'is_active', 'is_vendor', 'is_superuser']

    def my_image(self, user):
        if user.avatar:
            return mark_safe(f"<img width='200' height='100' src='{user.avatar.url}' />")

    def save_model(self, request, obj, form, change):
        if change and not form.cleaned_data['password']:
            return

            # Lấy mật khẩu từ form
        password = form.cleaned_data['password']

        # Mã hóa mật khẩu trước khi lưu
        if password:
            obj.set_password(password)

        super().save_model(request, obj, form, change)


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'following', 'followed', 'rating', 'user_id', 'my_image', 'active']
    search_fields = ['id', 'name']
    list_filter = ['active', 'rating']

    def my_image(self, shop):
        if shop.img:
            return mark_safe(f"<img width='200' height='200' src='{shop.img.url}' />")


class ProductInfoInline(admin.StackedInline):  # Hoặc InlineModelAdmin tùy thuộc vào giao diện bạn muốn
    model = ProductInfo
    extra = 1  # Số lượng form tạo mới ban đầu
    max_num = 1


class ProductImageDetailInline(admin.StackedInline):
    model = ProductImageDetail
    extra = 1
    max_num = 20


class ProductImagesColorInline(admin.StackedInline):
    model = ProductImagesColors
    extra = 1
    max_num = 20


class ProductVideosInline(admin.StackedInline):
    model = ProductVideos
    extra = 1
    max_num = 10


class ProductSellInline(admin.StackedInline):
    model = ProductSell
    extra = 1
    max_num = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'shop_id', 'category_name', 'my_image', 'active']
    search_fields = ['id', 'name']
    list_filter = ['category_id', 'shop_id', 'price']

    inlines = [ProductInfoInline, ProductImageDetailInline, ProductImagesColorInline, ProductVideosInline,
               ProductSellInline]

    def my_image(self, product):
        if product.img:
            return mark_safe(f"<img width='200' height='200' src='{product.img.url}' />")

    def category_name(self, product):
        category = Category.objects.get(id=product.category_id)
        return category.name


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'product_name', 'origin', 'material', 'manufacture']
    search_fields = ['id', 'manufacture']
    list_filter = ['origin', 'material', 'manufacture']

    def product_name(self, obj):
        return obj.product.name


class ProductImageDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'my_image']
    search_fields = ['id', 'product_id']
    list_filter = ['product_id']

    def my_image(self, product):
        if product.image:
            return mark_safe(f"<img width='200' height='200' src='{product.image.url}' />")


class ProductImagesColorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'name_color', 'my_image']
    search_fields = ['id', 'name_color']
    list_filter = ['product_id']

    def my_image(self, product):
        if product.url_image:
            return mark_safe(f"<img width='200' height='200' src='{product.url_image.url}' />")


class ProductVideosAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'my_video']
    search_fields = ['id']
    list_filter = ['product_id']

    def my_video(self, product):
        if product.url_video:
            return mark_safe(f"<img width='200' height='200' src='{product.url_video.url}' />")


class VoucherConditionInline(admin.StackedInline):
    model = VoucherCondition
    extra = 1
    max_num = 1


class VoucherAdmin(admin.ModelAdmin):
    list_display = ['id', 'my_image', 'name', 'code', 'all_time_used', 'description', 'active']
    search_fields = ['id', 'name', 'code']
    list_filter = ['name']

    inlines = [VoucherConditionInline]

    def my_image(self, voucher):
        if voucher.img:
            return mark_safe(f"<img width='100' height='100' src='{voucher.img.url}' />")


class VoucherConditionAdmin(admin.ModelAdmin):
    list_display = ['id', 'voucher_id', 'order_fee_min', 'voucher_sale', 'voucher_sale_max', 'time_usable',
                    'time_expired']
    search_fields = ['id', 'time_usable', 'time_expired']
    list_filter = ['id', 'order_fee_min', 'voucher_sale_max', 'time_usable', 'time_expired']


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(ProductImageDetail, ProductImageDetailAdmin)
admin.site.register(ProductImagesColors, ProductImagesColorsAdmin)
admin.site.register(ProductVideos, ProductVideosAdmin)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(VoucherCondition, VoucherConditionAdmin)
