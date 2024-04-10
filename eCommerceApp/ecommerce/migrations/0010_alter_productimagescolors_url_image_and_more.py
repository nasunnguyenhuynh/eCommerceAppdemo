# Generated by Django 5.0.4 on 2024-04-10 03:34

import cloudinary.models
import ecommerce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0009_productimagedetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimagescolors',
            name='url_image',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='productvideos',
            name='url_video',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, validators=[ecommerce.models.validate_video_size]),
        ),
    ]