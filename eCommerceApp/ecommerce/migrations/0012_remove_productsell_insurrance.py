# Generated by Django 5.0.4 on 2024-04-10 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_alter_productsell_percent_sale_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsell',
            name='insurrance',
        ),
    ]
