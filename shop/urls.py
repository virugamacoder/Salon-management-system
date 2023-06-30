from django.urls import path
from . import views

app_name = 'myapp_shop'

urlpatterns = [
    path('addcart/<int:pid>/', views.addcart, name="addcart"),
    path('addcartplus/<int:pid>/', views.addcartplus, name="addcartplus"),
    path('removecartminus/<int:pid>/', views.removecartminus, name="removecartminus"),
    path('removecart/<int:pid>/', views.removecart, name="removecart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('bookorder/', views.bookorder, name="bookorder"),
    path('finish/', views.finish, name="finish"),
    path('shop/', views.shop, name="shop"),
    path('single-product/<int:pid>/', views.single_prod, name="single_prod")
]