from timeit import default_timer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import GroupForm
from .models import Product, Order, Profile
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "good_shop/register.html"
    success_url = reverse_lazy("good_shop:about_user")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)

        return response


class AboutMeView(TemplateView):
    template_name = "good_shop/about_me.html"


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


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "good_shop.add_product"

    # def test_func(self):
    #     # return self.request.user.groups.filter(name="secret_group").exists()
    #     return self.request.user.permission
    model = Product
    fields = "name", "price", "description", "discount"
    # form_class = GroupForm
    success_url = reverse_lazy("good_shop:products")

    def form_valid(self, form):
        pass


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


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


# def order_list(request: HttpRequest):
#     context = {
#         'order': Order.objects.select_related('user').prefetch_related('products').all(),
#     }
#     return render(request, template_name='good_shop/order_list.html', context=context)


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "good_shop.view_order"
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


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("good_shop:index")

        return render(request, 'good_shop/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("good_shop:index")

    return render(request, 'good_shop/login.html', context={'error': "Неверное имя пользователя или пароль"})

@user_passes_test(lambda user:user.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default")
    return HttpResponse(f"Cookie value {value!r}")

@permission_required("good_shop.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foo"] = "bar"
    return HttpResponse("Сессия установлена")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foo", "default")
    return HttpResponse(f"Session value {value}")

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("good_shop:login"))

# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("good_shop:index")