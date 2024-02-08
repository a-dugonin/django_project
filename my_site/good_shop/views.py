from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group
from .models import Product, Order
from .forms import ProductForm


# Create your views here.
def good_shop_index(request: HttpRequest):
    products = [('Яблоки', 150), ('Апельсины', 200), ('Бананы', 150)]
    context = {'time_run': default_timer(), 'products': products}
    return render(request, 'good_shop/shop_index.html', context=context)


def good_shop_groups(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),

    }
    return render(request, 'good_shop/group_list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        'product': Product.objects.all(),
    }
    return render(request, 'good_shop/products_list.html', context=context)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        my_form = ProductForm(request.POST)
        if my_form.is_valid():
            # name = my_form.cleaned_data['name']
            # price = my_form.cleaned_data['price']
            Product.objects.create(**my_form.cleaned_data)
            url = reverse("good_shop:products")
            return redirect(url)
    else:
        my_form = ProductForm()
        context = {
            'product_form': my_form
        }
        return render(request, template_name='good_shop/create_product.html', context=context)


def order_list(request: HttpRequest):
    context = {
        'order': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    return render(request, template_name='good_shop/order_list.html', context=context)
