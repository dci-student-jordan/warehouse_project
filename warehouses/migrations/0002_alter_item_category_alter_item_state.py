# Generated by Django 5.0.2 on 2024-03-05 13:41

import warehouses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=warehouses.models._get_category_choices, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='state',
            field=models.CharField(choices=warehouses.models._get_state_choices, max_length=100),
        ),
    ]
