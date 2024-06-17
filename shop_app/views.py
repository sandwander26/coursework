import uuid

from django.db.models import F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, CreateView
from .forms import OrderForm
from .models import FlowerList, Cart, Order, Promocode
from .models import FlowerList


class MainPageView(View):
    @method_decorator(cache_page(60 * 30))
    def get(self, request):
        flowers = FlowerList.objects.all().order_by('-number_of_uses').filter(category='bouquet')

        context = {
            'flowers_popular': flowers[:4],
            'flowers': flowers.order_by('number_of_uses')
        }
        return render(request, 'shop_app/color_shop.html', context)

@method_decorator(cache_page(60 * 30), name='dispatch')
class FlowerDetailsView(View):
    def get(self, request, pk):
        flower = FlowerList.objects.filter(pk=pk)

        context = {
            "flower": flower[0],
        }
        return render(request, 'shop_app/flower_details.html', context)


@require_POST
def add_to_cart(request, pk):
    flower = get_object_or_404(FlowerList, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(flower)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
def delete_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    flower = get_object_or_404(FlowerList, pk=pk)
    cart.products.remove(flower)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CartPageView(View):
    def get(self, request):
        products_info = []  # Создаем список для хранения информации о товарах в корзине

        current_user = request.user #Получение актуального пользователя
        if current_user.is_authenticated:
            cart = Cart.objects.filter(user=current_user).prefetch_related("products")

            for item in cart:
                for product in item.products.all():
                    # Добавляем информацию о товаре в список products_info
                    products_info.append({
                        'flower_name': product.name,
                        'flower_pk': product.pk,
                        'flower_price': product.price,
                        'flower_image': product.image,
                        'flower_description': product.description,
                    })
        else:
            cart = None

        context = {
            'cart': cart,
            'products_info': products_info,  # Передаем информацию о товарах в контекст
        }

        return render(request, 'shop_app/cart_details.html', context)

    def post(self, request):
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                delivery_adress = request.POST.get('delivery_adress')
                promocode = request.POST.get('promocode')
                phone = request.POST.get('phone')

                order = Order.objects.create(delivery_adress=delivery_adress,
                                             phone=phone,
                                             promocode=promocode,
                                             user_id=request.user.id
                                             )

                final_sum = 0
                cart = Cart.objects.filter(user=request.user).prefetch_related("products")
                for item in cart:
                    for product in item.products.all():
                        order.products.add(product)
                        final_sum += int(product.price)
                        FlowerList.objects.filter(id=product.id).update(number_of_uses=F('number_of_uses') + 1)

                Cart.objects.filter(user_id=request.user.id).delete()

                if promocode is not None:
                    promocode = Promocode.objects.filter(text=promocode).first()
                    if promocode is not None:
                        discount = promocode.count
                        final_sum = round(final_sum * (100 - discount) / 100)

                order.final_sum = final_sum
                order.save()

                return redirect(reverse('shop_app:order_details', kwargs={"pk": order.pk}))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class OrderDetailView(View):
    def get(self, request, pk):
        current_user = request.user

        order = Order.objects.filter(pk=pk).prefetch_related("products").first()

        if order.user.username == current_user.username:
            products = order.products.all()

            context = {
                "pk": pk,
                "products": products,
            }
            return render(request, 'shop_app/order_details.html', context)
        else:
            return redirect("shop_app:shop_app")

class SearchView(View):
    def get(self, request):
        search = request.GET.get("search")

        if search:
            result_flowers = FlowerList.objects.filter(name__icontains=search)[:4]

            context = {
                "flowers_list": result_flowers,
            }
        else:
            context = {
                "flowers_list": [],
            }

        return render(request, 'shop_app/search_view.html', context)

