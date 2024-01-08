from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Category',  on_delete=models.SET_NULL, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name