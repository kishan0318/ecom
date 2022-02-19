from os import name
from django.urls import path,include
from .views import *

app_name="ecomapp1"

urlpatterns = [
    path("",Home.as_view(),name='home'),
    path("about",about,name='about'),
    path("signup",Signup.as_view(),name='register'),
    path("login",Signin.as_view(),name='login'),
    path("<int:pk>",Dts.as_view(),name='items'),
    path("signout",signout,name='logout'),
    path("StaffLogin",StaffLogin.as_view(),name='loginstaff'),
    path("Add-product/",Add_Product.as_view(),name='addproduct'),
    path("Product/update/<int:pk>/",Up_Product.as_view(),name='upproduct'),
    path("Product/delete/<int:pk>/",Del_product.as_view(),name='delproduct'),
    path("Product/items/add/<int:pk>",AddItem.as_view(),name='additems'),
    path("Product/items/delete/<int:pk>",DelItem.as_view(),name='delitem'),
    path("app1/api/",include('ecomapp1.api.urls',namespace='ecomapp1')),
    path("items/<int:pk>",Dts1.as_view(),name='Dts1'),
    path("items/home",action,name="items/home"),
    path('add_cart/<int:pk>',add_to_cart,name='cart'),
    path('cart/',show_cart, name='show_cart'),
    path('delete/<int:pk>',DelCart.as_view(),name='delcart'),
     path('payment',payment,name='payment')
      
]