from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin
from .models import Category, User, Product, Shop, ProductInfo


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


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'following', 'followed', 'rating', 'user_id', 'my_image', 'active']
    search_fields = ['id', 'name']
    list_filter = ['active', 'rating']

    def my_image(self, shop):
        if shop.img:
            return mark_safe(f"<img width='200' height='200' src='{shop.img.url}' />")


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'shop_id', 'category_name', 'my_image', 'active']
    search_fields = ['id', 'name']
    list_filter = ['category_id', 'shop_id', 'price']

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
