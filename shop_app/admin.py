import csv

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, reverse

from .models import FlowerList, Cart, Order, Promocode
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(FlowerList)
class FlowerAdmin(admin.ModelAdmin):
    search_fields = "name", "id"
    actions = [
        mark_archived,
        mark_unarchived,
    ]

    list_display = "pk", "name", "description_short", "archived", "number_of_uses"
    list_display_links = "pk", "name"
    ordering = ("id",)

    fieldsets = [
        (None, {
           "fields": ("name", "description")
        }),
        ("Price options", {
            "fields": ("price", "number_of_uses")
        }),
        ("Extra options", {
            "fields": ("archived", "category", "image"),
            "classes": ("collapse",),
            "description": "Дополнительные опции"
        }),
    ]

    def description_short(self, obj: FlowerList) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ("products__name", "products__id",)
    list_display = "pk", "user", "display_products"
    list_display_links = "pk", "user"
    ordering = ("id",)

    def display_products(self, obj):
        return ', '.join(product.name for product in obj.products.all())

    display_products.short_description = 'Товары в корзине'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shop_app/products_changelist.html"
    search_fields = ("products__name", "products__id",)
    list_display = "pk", "delivery_adress", "phone", "created_at", "final_sum"
    list_display_links = "pk",
    ordering = ("id",)

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response, lineterminator="\r\n")
        writer.writerow(['ID', 'DelAdr', 'Promocode', 'Phone', 'User_ID', 'ID_Products', 'Final_Sum'])

        queryset = Order.objects.all().select_related("user").prefetch_related("products")
        for obj in queryset:
            products = ', '.join(str(id) for id in obj.products.values_list("id", flat=True))
            writer.writerow([obj.id, obj.delivery_adress, obj.promocode, obj.phone, obj.user_id, products, obj.final_sum])

        return response


    def import_csv(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                return HttpResponseRedirect(reverse('admin:shop_app_order_changelist') + '?error=file_not_csv')

            if csv_file.size > 10 * 1024:
                return HttpResponseRedirect(reverse('admin:shop_app_order_changelist') + '?error=file_too_large')

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                try:
                    id, deladr, promocode, phone, user_id, id_products, final_sum = row.values()
                    id_products = [item.strip() for item in id_products.split(',')]

                    order, created = Order.objects.get_or_create(
                        id=id,
                        phone=phone,
                        delivery_adress=deladr,
                        user_id=user_id,
                        final_sum=final_sum
                    )

                    if created == True:
                        for product_id in id_products:
                            order.products.add(product_id)

                except:
                    continue

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("export-products-scv/", self.export_csv, name="export_products_csv"),
            path("import-products-csv/", self.import_csv, name="import_products_csv"),
        ]
        return new_urls + urls


class CustomUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'get_orders')
    list_display_links = ("pk", "username")

    def get_orders(self, obj):
        return Order.objects.filter(user=obj).count()

    def orders_list(self, obj):
        orders = Order.objects.filter(user=obj)
        orders_info = []
        for order in orders:
            order_info = ', '.join(f"ID: {product.pk}, {product.name}" for product in order.products.all().selected_related("user").prefetch_related("products"))
            orders_info.append(f"Состав заказа: {order.pk} - {order_info}\n")
        return ''.join(orders_info)

    get_orders.short_description = 'Количество заказов'

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('orders_list',),
        }),
    )

    readonly_fields = ('orders_list',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Promocode)