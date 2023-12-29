from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import Product, Order


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


def order_list(request: HttpRequest):
    context = {
        'order': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    return render(request, template_name='good_shop/order_list.html', context=context)
