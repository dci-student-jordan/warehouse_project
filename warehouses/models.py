from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    '''Model for employees'''
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    head_of = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self) -> str:
        return self.name


class Warehouse(models.Model):
    '''Model for the warehouses'''
    name = models.CharField(max_length=100)


class Item(models.Model):
    '''Model For warehouse Items'''
    state = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    date_of_stock = models.DateTimeField()


class Contact(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

