from django.db import models
from django.contrib.auth.models import User
from cli.toys import glued_string
from django.core.exceptions import ValidationError
import json

# Create your models here.

class Employee(models.Model):
    '''Model for employees'''
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    head_of = models.ManyToManyField('self', symmetrical=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Warehouse(models.Model):
    '''Model for the warehouses'''
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

def validate_dimensions(value):
    # If value is None, it's valid
    if value is None:
        return
    
    # Check if all keys other than 'height', 'width', and 'depth' are absent
    allowed_keys = {'height', 'width', 'depth'}
    for key in value.keys():
        if key not in allowed_keys:
            raise ValidationError(f"Invalid key '{key}' found. Only 'height', 'width', and 'depth' are allowed.")


class Item(models.Model):
    '''Model For warehouse Items'''
    state = models.CharField(max_length=100, choices=[('', 'Select State')])
    category = models.CharField(max_length=100, choices=[('', 'Select Category')])
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    date_of_stock = models.DateTimeField()
    name = models.CharField(max_length=100, null=True)
    dimensions = models.JSONField(null=True, blank=True, validators=([validate_dimensions]))


    def get_state_choices(self):
        return self.get_choices('state')

    def get_category_choices(self):
        return self.get_choices('category')

    def get_choices(self, field_name):
        return [(value, value) for value in Item.objects.values_list(field_name, flat=True).distinct()]



    def get_default_item_name(self, state, category):
        if category[-1] != "s":
            return f"{glued_string(state)} {category.lower()}"
        else:
            return f"{state} {category.lower()}"

    def save(self, *args, **kwargs):
        print("Try setting name")
        if not self.name:
            self.name = self.get_default_item_name(self.state, self.category)
            print("setting name:", self.name)
        super().save(*args, **kwargs)



class Contact(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

