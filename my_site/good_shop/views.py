from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import GroupForm
from .models import Product, Order


class GoodShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [('Яблоки', 150), ('Апельсины', 200), ('Бананы', 150)]
        context = {'time_run': default_timer(), 'products': products}
        return render(request, 'good_shop/shop_index.html', context=context)


class GoodShopGroupsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'good_shop/group_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "good_shop/product_details.html"
    model = Product
    context_object_name = "product"
    # def get(self, request: HttpRequest, key: int) -> HttpResponse:
    #     product = get_object_or_404(Product, pk=key)
    #     context = {
    #         "product": product
    #     }
    #     return render(request, "good_shop/product_details.html", context=context)


class ProductsListView(ListView):
    template_name = 'good_shop/products_list.html'
    # model = Product
    context_object_name = "product"
    queryset = Product.objects.filter(archived=False)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["product"] = Product.objects.all()
    #     return context


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    # form_class = GroupForm
    success_url = reverse_lazy("good_shop:products")


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         my_form = ProductForm(request.POST)
#         if my_form.is_valid():
#             # name = my_form.cleaned_data['name']
#             # price = my_form.cleaned_data['price']
#             # Product.objects.create(**my_form.cleaned_data)
#             my_form.save()
#             url = reverse("good_shop:products")
#             return redirect(url)
#     else:
#         my_form = ProductForm()
#         context = {
#             'product_form': my_form
#         }
#         return render(request, template_name='good_shop/product_form.html', context=context)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount", "archived"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("good_shop:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("good_shop:products")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


# def order_list(request: HttpRequest):
#     context = {
#         'order': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, template_name='good_shop/order_list.html', context=context)


class OrderDetailView(DetailView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrderCreateView(CreateView):
    template_name = 'good_shop/order_form.html'
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    fields = "user", "delivery_address", "products", "promo"
    success_url = reverse_lazy("good_shop:orders")


# def order_create(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("good_shop:orders")
#             return redirect(url)
#     else:
#         form = OrderForm()
#         context = {
#             "order_form": form
#         }
#         return render(request, template_name='good_shop/order_form.html', context=context)

class OrderUpdateView(UpdateView):
    template_name = 'good_shop/order_update_form.html'
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    fields = "user", "delivery_address", "products", "promo"

    def get_success_url(self):
        return reverse("good_shop:orders_detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    success_url = reverse_lazy("good_shop:orders")
