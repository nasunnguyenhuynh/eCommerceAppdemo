# Generated by Django 5.0.4 on 2024-04-15 07:35

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0023_rename_status_statusconfirmationshop_status_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='rating',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]