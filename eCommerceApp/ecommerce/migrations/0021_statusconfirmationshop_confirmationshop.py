# Generated by Django 5.0.4 on 2024-04-11 03:42

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0020_remove_vouchertype_voucher_voucher_voucher_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusConfirmationShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmationShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_identification_image', cloudinary.models.CloudinaryField(max_length=255)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]