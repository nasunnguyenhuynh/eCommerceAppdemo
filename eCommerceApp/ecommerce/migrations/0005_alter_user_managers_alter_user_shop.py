# Generated by Django 5.0.4 on 2024-04-09 09:34

import django.contrib.auth.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_alter_user_user_details'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.shop'),
        ),
    ]