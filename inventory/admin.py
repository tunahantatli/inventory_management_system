from django.contrib import admin
from .models import InventoryItem, Category, Unit
# Register your models here.

@admin.register(InventoryItem)
class InventoryItemModelAdmin(admin.ModelAdmin):
    list_display=[
        "id",
        "name",
        "quantity",
        "unit",
        "category",
        "created_date",
        "user"
    ]

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        "name"
    ]

@admin.register(Unit)
class UnitModelAdmin(admin.ModelAdmin):
    list_display = [
        "name"
    ]