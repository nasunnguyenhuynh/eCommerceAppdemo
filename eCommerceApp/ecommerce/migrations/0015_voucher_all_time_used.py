# Generated by Django 5.0.4 on 2024-04-10 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0014_remove_voucher_condition_vouchercondition_voucher_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='all_time_used',
            field=models.IntegerField(default=0),
        ),
    ]
