from __future__ import unicode_literals
from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Supplier


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}')
            return redirect('users-registration')

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('p_name')
        product_price = request.POST.get('p_price')
        product_quantity = request.POST.get('p_quantity')
        # Save data into the database
        product = Product(prod_name=product_name,
                          prod_price=product_price,
                          prod_quantity=product_quantity)
        product.save()
        messages.success(request, "Data saved successfully")
        return redirect("add-product")

    return render(request, 'add-products.html')


@login_required
def view_products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect("products")


@login_required
def update_product(request, id):
    if request.method == "POST":
        # Receive updated data from the form
        product_name = request.POST.get("p_name")
        product_price = request.POST.get("p_price")
        product_quantity = request.POST.get("p_quantity")

        # Select the product you want to update
        product = Product.objects.get(id=id)

        # Update the product
        product.prod_name = product_name
        product.prod_quantity = product_quantity
        product.prod_price = product_price

        # Return the updated values back to the database
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('products')

    product = Product.objects.get(id=id)
    return render(request, 'update.html', {'product': product})


@login_required
def add_supplier(request):
    # Check if the form submitted has a method post
    if request.method == "POST":
        # Receive the data from the form
        name = request.POST.get('s_name')
        email = request.POST.get('s_email')
        phone = request.POST.get('s_phone')
        product = request.POST.get('s_product')

        # Finally save the data into the suppliers table
        supplier = Supplier(sup_name=name, sup_email=email,
                            sup_phone=phone, sup_product=product)
        supplier.save()
        # redirect back to add supplier page with a success message
        messages.success(request, 'Supplier added successfully')
        return redirect('add-supplier')
    return render(request, 'add-supplier.html')


@login_required
def view_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers.html', {'suppliers': suppliers})


@login_required
def delete_supplier(request, id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()
    messages.success(request, 'Supplier deleted successfully')
    return redirect('suppliers')


@login_required
def update_supplier(request, id):
    supplier = Supplier.objects.get(id=id)
    if request.method == "POST":
        updated_name = request.POST.get('s_name')
        updated_email = request.POST.get('s_email')
        updated_phone = request.POST.get('s_phone')
        updated_product = request.POST.get('s_product')

        supplier.sup_name = updated_name
        supplier.sup_email = updated_email
        supplier.sup_phone = updated_phone
        supplier.sup_product = updated_product

        supplier.save()
        return redirect('suppliers')
    return render(request, 'update-supplier.html', {'supplier': supplier})


# Instantiate the MpesaClient
cl = MpesaClient()
# Prepare transaction callbacks
stk_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = "https://api.darajambili.com/b2c/result"


# Prepare a function to generate transaction auth token
def auth_success(request):
    token = cl.access_token()
    return JsonResponse(token, safe=False)


@login_required
def pay(request, id):
    # Select the product being paid for
    product = Product.objects.get(id=id)
    if request.method == "POST":
        phone_number = request.POST.get('nambari')
        amount = request.POST.get('pesa')
        amount = int(amount)
        account_ref = "WANYAMA"
        transaction_desc = "Payment for goods"
        transaction = cl.stk_push(phone_number, amount, account_ref,
                                  transaction_desc, stk_callback_url)
        return JsonResponse(transaction.response_description, safe=False)
    return render(request, 'payment.html', {'product': product})
