from django.urls import path
from .views import *

app_name = 'ecomapp1'

urlpatterns=[
    path('SignupAPIView',SignupAPIView.as_view()),
    path("login",LoginAPIView.as_view(),name='Login'),
    path('view_products',ProductsAPIView.as_view()),
    path('create_or_view_product',ProductCreateApi.as_view()),
    path("update/<int:pk>",ProductsUpAPIView.as_view(),name='update'),

    path("delete/<int:pk>",DeleteProductsAPIView.as_view(),name='delete1'),

    path("items/",ItemsAPIView.as_view(),name='items'),

    path('create_items/',ItemsCreateAPIView.as_view()),

    path('updelitem/<int:pk>/',UpdelitemView.as_view(),name='itemupdel'),

    path("cart",CartListView.as_view(),name='cartviewadmin'),

    path('place_order',OrderApiView.as_view(),name='orderplace'),

    path('payment',PaymentApiView.as_view(),name='payment'),
    
    path('cart1',Cart1.as_view(),name='cart1'),
   
   
]