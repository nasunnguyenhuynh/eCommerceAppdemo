# Generated by Django 5.0.4 on 2024-04-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_remove_user_shop_shop_user_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]