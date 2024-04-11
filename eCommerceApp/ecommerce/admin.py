from cloudinary.models import CloudinaryField
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin
from .models import Category, User, Product, Shop, ProductInfo, ProductImageDetail, ProductImagesColors, ProductVideos, \
    ProductSell, Voucher, VoucherCondition, VoucherType, ConfirmationShop, StatusConfirmationShop
from django.contrib.auth.models import Group


class CustomGroupAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        # Kiểm tra nếu người dùng không phải là superuser
        if not request.user.is_superuser:
            # Nếu không phải là superuser, không cho phép xem bảng Group
            return False
        # Trả về giá trị mặc định nếu là superuser
        return True

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class AdminGroupManager(admin.ModelAdmin):

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='CATEGORY_MANAGER').exists() and "ecommerce.view_category" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if request.user.groups.filter(
                name='CATEGORY_MANAGER').exists() and "ecommerce.add_category" in request.user.get_user_permissions() or request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(
                name='CATEGORY_MANAGER').exists() and "ecommerce.change_category" in request.user.get_user_permissions() or request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(
                name='CATEGORY_MANAGER').exists() and "ecommerce.delete_category" in request.user.get_user_permissions() or request.user.is_superuser:
            return True
        return False


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'birthday', 'is_active', 'is_vendor',
                    'is_superuser',
                    'my_image']
    search_fields = ['id', 'username']
    list_filter = ['id', 'is_active', 'is_vendor', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'avatar', 'password')}),
        ('Login info', {'fields': ('date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birthday', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def my_image(self, user):
        if user.avatar:
            return mark_safe(f"<img width='200' height='100' src='{user.avatar.url}' />")

    def save_model(self, request, obj, form, change):

        if change and "pbkdf2_sha256" in form.cleaned_data['password']:
            super().save_model(request, obj, form, change)
        else:
            password = form.cleaned_data['password']
            # Mã hóa mật khẩu trước khi lưu
            if password:
                obj.set_password(password)
                super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='USER_MANAGER').exists() and "ecommerce.view_user" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='USER_MANAGER').exists() and "ecommerce.add_user" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='USER_MANAGER').exists() and "ecommerce.change_user" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='USER_MANAGER').exists() and "ecommerce.delete_user" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


class ShopAdmin(AdminGroupManager):
    list_display = ['id', 'name', 'following', 'followed', 'rating', 'user_id', 'my_image', 'active']
    search_fields = ['id', 'name']
    list_filter = ['active', 'rating']

    def my_image(self, shop):
        if shop.img:
            return mark_safe(f"<img width='200' height='200' src='{shop.img.url}' />")

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='SHOP_MANAGER').exists() and "ecommerce.view_shop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='SHOP_MANAGER').exists() and "ecommerce.add_shop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='SHOP_MANAGER').exists() and "ecommerce.change_shop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='SHOP_MANAGER').exists() and "ecommerce.delete_shop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


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


class ProductAdmin(AdminGroupManager):
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

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.view_product" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.add_product" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.change_product" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.delete_product" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


class ProductInfoAdmin(AdminGroupManager):
    list_display = ['id', 'product_id', 'product_name', 'origin', 'material', 'manufacture']
    search_fields = ['id', 'manufacture']
    list_filter = ['origin', 'material', 'manufacture']

    def product_name(self, obj):
        return obj.product.name

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.view_product_info" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.add_product_info" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.change_product_info" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='PRODUCT_MANAGER').exists() and "ecommerce.delete_product_info " in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


class ProductImageDetailAdmin(AdminGroupManager):
    list_display = ['id', 'product_id', 'my_image']
    search_fields = ['id', 'product_id']
    list_filter = ['product_id']

    def my_image(self, product):
        if product.image:
            return mark_safe(f"<img width='200' height='200' src='{product.image.url}' />")


class ProductImagesColorsAdmin(AdminGroupManager):
    list_display = ['id', 'product_id', 'name_color', 'my_image']
    search_fields = ['id', 'name_color']
    list_filter = ['product_id']

    def my_image(self, product):
        if product.url_image:
            return mark_safe(f"<img width='200' height='200' src='{product.url_image.url}' />")


class ProductVideosAdmin(AdminGroupManager):
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


class VoucherTypeAdmin(AdminGroupManager):
    list_display = ['id', 'name', 'key']
    search_fields = ['id', 'name', 'key']
    list_filter = ['name']


class VoucherAdmin(AdminGroupManager):
    list_display = ['id', 'my_image', 'name', 'code', 'maximum_time_used', 'description', 'active']
    search_fields = ['id', 'name', 'code']
    list_filter = ['name']

    inlines = [VoucherConditionInline]

    def my_image(self, voucher):
        if voucher.img:
            return mark_safe(f"<img width='100' height='100' src='{voucher.img.url}' />")

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='VOUCHER_MANAGER').exists() and "ecommerce.view_voucher" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='VOUCHER_MANAGER').exists() and "ecommerce.add_voucher" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='VOUCHER_MANAGER').exists() and "ecommerce.change_voucher" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='VOUCHER_MANAGER').exists() and "ecommerce.delete_voucher" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


class VoucherConditionAdmin(AdminGroupManager):
    list_display = ['id', 'voucher_id', 'order_fee_min', 'voucher_sale', 'voucher_sale_max', 'time_usable',
                    'time_expired']
    search_fields = ['id', 'time_usable', 'time_expired']
    list_filter = ['id', 'order_fee_min', 'voucher_sale_max', 'time_usable', 'time_expired']


class StatusConfirmationShopAdmin(AdminGroupManager):
    list_display = ['id', 'status_content']
    search_fields = ['id', 'status_content']
    list_filter = ['status_content']

    def has_view_permission(self, request, obj=None):
        print(request.user.get_user_permissions())
        if (request.user.groups.filter(
                name='CONFIRMATION_SHOP_MANAGER').exists() and "ecommerce.view_statusconfirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(
                name='CONFIRMATION_SHOP_MANAGER').exists() and "ecommerce.add_statusconfirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='CONFIRMATION_SHOP_MANAGER').exists() and "ecommerce.change_statusconfirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(
                name='CONFIRMATION_SHOP_MANAGER').exists() and "ecommerce.delete_statusconfirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


class ConfirmationShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'citizen_identification_image1', 'avatar', 'username', 'birthday', 'phone', 'status_content1',
                    'note']
    search_fields = ['username', 'phone']
    list_filter = ['status_id']

    fieldsets = (
        ("Results", {'fields': ('status', 'note',)}),

    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs[
                'queryset'] = StatusConfirmationShop.objects.all()
            kwargs[
                'to_field_name'] = 'status_content'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def avatar(self, confirmationshop):
        user = User.objects.get(id=confirmationshop.user_id)
        if user.avatar:
            return mark_safe(
                f"<img width='100' height='100' src='{user.avatar.url}' />")

    def citizen_identification_image1(self, confirmationshop):
        if confirmationshop.citizen_identification_image:
            return mark_safe(
                f"<img width='200' height='100' src='{confirmationshop.citizen_identification_image.url}' />")

    def status_content1(self, confirmationshop):
        status = StatusConfirmationShop.objects.get(id=confirmationshop.status_id)
        return status.status_content

    def username(self, confirmationshop):
        user = User.objects.get(id=confirmationshop.user_id)
        return user.username

    def birthday(self, confirmationshop):
        user = User.objects.get(id=confirmationshop.user_id)
        return user.birthday

    def phone(self, confirmationshop):
        user = User.objects.get(id=confirmationshop.user_id)
        return user.phone

    def has_view_permission(self, request, obj=None):
        if (request.user.groups.filter(name='CONFIRMATION_SHOP_MANAGER').exists()
                and "ecommerce.view_confirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        if (request.user.groups.filter(name='CONFIRMATION_SHOP_MANAGER').exists()
                and "ecommerce.add_confirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if (request.user.groups.filter(name='CONFIRMATION_SHOP_MANAGER').exists()
                and "ecommerce.change_confirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.groups.filter(name='CONFIRMATION_SHOP_MANAGER').exists()
                and "ecommerce.delete_confirmationshop" in request.user.get_user_permissions()
                or request.user.is_superuser):
            return True
        return False


admin.site.register([User], CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(ProductImageDetail, ProductImageDetailAdmin)
admin.site.register(ProductImagesColors, ProductImagesColorsAdmin)
admin.site.register(ProductVideos, ProductVideosAdmin)
admin.site.register(VoucherType, VoucherTypeAdmin)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(VoucherCondition, VoucherConditionAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(StatusConfirmationShop, StatusConfirmationShopAdmin)
admin.site.register(ConfirmationShop, ConfirmationShopAdmin)
