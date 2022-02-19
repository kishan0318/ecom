from django.urls import path
from .views import *

app_name = 'ecomapp1'

urlpatterns=[
    path("login",LoginAPIView.as_view(),name='Login'),
    path('products',ProductsAPIView.as_view()),
    path('products1',ProductsAPIView1.as_view()),
    path("update/<int:pk>",ProductsUpAPIView.as_view(),name='update'),
    path("delete/<int:pk>",DeleteProductsAPIView.as_view(),name='delete1'),
    path("items",ItemsAPIView.as_view(),name='items'),
    path('updelitem/<int:pk>',UpdelitemView.as_view(),name='itemupdel'),
    path("cart",CartListView.as_view(),name='cartviewadmin'),

    path('place_order',OrderApiView.as_view(),name='orderplace'),
    path('payment',PaymentApiView.as_view(),name='payment'),
    path('cart1',Cart1.as_view(),name='cart1'),
   
   
]