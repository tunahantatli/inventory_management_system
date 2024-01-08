from django.urls import path
from .views import Index, RegisterView, LogoutView, DashboardView, AddItem, EditItem, DeleteItem, CategoryView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-view'),
    path('register/', RegisterView.as_view(), name="register"),
    path('add-item/', AddItem.as_view(), name="add-item"),
    path('edit-item/<int:pk>', EditItem.as_view(), name="edit-item"),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name="delete-item"),
    path('login/', auth_views.LoginView.as_view(template_name="inventory/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]