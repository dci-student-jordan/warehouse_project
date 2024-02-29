# Generated by Django 5.0.2 on 2024-02-27 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0007_delete_employeeworkinghours'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeWorkingHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouses.employee')),
            ],
        ),
    ]