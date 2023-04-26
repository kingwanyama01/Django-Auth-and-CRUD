"""afternoonDjangoRegistration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views as general_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', general_views.register, name='users-registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='user-login'),
    path('home/', general_views.home, name='my-home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='user-logout'),
    path('add-product/', general_views.add_product, name='add-product'),
    path('products/', general_views.view_products, name='products'),
    path('delete-product/<id>', general_views.delete_product, name='delete-product'),
    path('update-product/<id>', general_views.update_product, name='update-product'),
    path('add-supplier/', general_views.add_supplier, name='add-supplier'),
    path('suppliers/', general_views.view_suppliers, name='suppliers'),
    path('delete-supplier/<id>', general_views.delete_supplier, name='delete-supplier'),
    path('update-supplier/<id>', general_views.update_supplier, name='update-supplier'),
    path('payment/<id>', general_views.pay, name='payment'),
]
