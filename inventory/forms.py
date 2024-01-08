from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InventoryItem, Category, Unit


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class InventoryItemForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
#     class Meta :
#         model = InventoryItem
#         fields = ["id", "name", "quantity", "category"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']


class InventoryItemForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=False,
        empty_label="Select existing unit",
    )
    new_unit_name = forms.CharField(
        max_length=10, required=False, label="Or enter new unit")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select existing category",
    )
    new_category_name = forms.CharField(
        max_length=200, required=False, label="Or enter new category")

    class Meta:
        model = InventoryItem
        fields = ["name", "quantity", "unit", "category"]

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('unit')
        new_unit_name = cleaned_data.get('new_unit_name')
        category = cleaned_data.get('category')
        new_category_name = cleaned_data.get('new_category_name')

        if not unit and not new_unit_name:
            raise forms.ValidationError(
                "Please select an existing unit or enter a new one.")
        if not category and not new_category_name:
            raise forms.ValidationError(
                "Please select an existing category or enter a new one.")

        return cleaned_data
