from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category, Unit
from main.settings import LOW_QUANTITY
from django.contrib import messages

# Create your views here.
class Index(TemplateView):
    template_name = "inventory/index.html"


class CategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        items_in_category = InventoryItem.objects.filter(user=self.request.user, category=category)
        
        return render(request, "inventory/category.html", {"category": category, "items_in_category": items_in_category})
    
    login_url = "/login/"

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')
        low_inventory = InventoryItem.objects.filter(
            user = self.request.user.id,
            quantity__lte=LOW_QUANTITY
        )
        if low_inventory.count() > 0:
            if low_inventory.count()>1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} items has low inventory')

        low_inventory_ids = InventoryItem.objects.filter(
            user = self.request.user.id,
            quantity__lte=LOW_QUANTITY
        ).values_list('id', flat=True)

        return render(request, "inventory/dashboard.html", {"items":items, "low_inventory_ids": low_inventory_ids})
    login_url = "/login/"



class AddItem(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        new_unit_name = self.request.POST.get('new_unit_name')
        if new_unit_name:
            unit = Unit.objects.create(name=new_category_name)
            form.instance.unit = unit
        new_category_name = self.request.POST.get('new_category_name')
        if new_category_name:
            category = Category.objects.create(name=new_category_name)
            form.instance.category = category
        form.instance.user = self.request.user
        return super().form_valid(form)



class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = "inventory/delete_item.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "item"






class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "inventory/register.html", {'form' : form})
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user  = authenticate(username= form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("index")
        return render(request, "inventory/register.html", {'form':form})
    

    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
