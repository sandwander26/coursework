from django.urls import path
from . import views

app_name = "shop_app"

urlpatterns = [
    path('', views.MainPageView.as_view(), name = "shop_app"),
    path('search/', views.SearchView.as_view(), name = "search"),
    path('details/<int:pk>/', views.FlowerDetailsView.as_view(), name='details'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:pk>/', views.delete_from_cart, name='delete_from_cart'),
    path('order_details/<int:pk>/', views.OrderDetailView.as_view(), name="order_details"),
    path('cart/', views.CartPageView.as_view(), name='cart'),
]
