from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order
from .admin_mixins import ExportCSVMixin


class OrderInLine(admin.TabularInline):
    model = Product.order.through


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv'
    ]
    inlines = [
        OrderInLine,
    ]
    list_display = 'pk', 'name', 'price', 'description_short', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {'fields': ('name', 'description'),
                }),
        ('Price_options', {'fields': ('price', 'discount'),
                           'classes': ('wide', 'collapse')}),
        ('Extra_options', {'fields': ('archived',),
                           'classes': ('collapse',),
                           'description': 'Для мягкого удаления'})
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 30:
            return obj.description
        return obj.description[:20] + '...'


class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine,
    ]
    list_display = 'delivery_address', 'promo', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
