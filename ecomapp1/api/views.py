from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from ..models import Products,Items
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

# Create your views here.

#login Apiview
class LoginAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer=LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success':'login successfully','data':serializer.data},status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

#any user can viwe the products
class ProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Products.objects.all()
    serializer_class = ProductsSer

#only admin user can view and create products
class ProductsAPIView1(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser,]
    queryset = Products.objects.all()
    serializer_class = ProductsSer1

#only admin user can update products
class ProductsUpAPIView(generics.UpdateAPIView):
    permission_classes =[IsAdminUser,]
    queryset = Products.objects.all()
    serializer_class=ProductsUpSer

#admin user acn update or delete/update products using this RetrieveUpdateDestroyAPIView view 
class DeleteProductsAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthenticated,]
    queryset = Products.objects.all()
    serializer_class = DelProductsSer


'''class DeleteAPIView2(APIView):
    permission_classes =[IsAuthenticated,]
    def delete(self,request,**kwargs):
        try:
            user = Products.objects.get(pk=self.kwargs.get('pk'))
            return Response({'Success':'user deleted successfully'},status=HTTP_200_OK)
        
        except Exception as e:
            return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)'''

#anyone can view items
class ItemsAPIView(generics.ListAPIView):
    permission_classes=[AllowAny,]
    queryset=Items.objects.all()
    serializer_class=ListItemSer

#only admin can create items
class ItemsAPIView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Items.objects.all()
    serializer_class=ListItemSer

#only admin can update/delete items
class UpdelitemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Items.objects.all()
    serializer_class= UpdelitemSer

#only admin user can add or view the cart
class CartListView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Cart.objects.all()
    serializer_class=CartSer

#only admin user can add or view the Order
class OrderApiView(generics.ListCreateAPIView):
    permission_classes =[IsAuthenticated,]
    queryset = Order.objects.all()
    serializer_class=OrderSer

class PaymentApiView(generics.CreateAPIView):
    permission_classes =[IsAuthenticated,]
    queryset = Payment.objects.all()
    serializer_class=PaymentSer

#only authenticated user can add to cart (authenticate:- using token)
class Cart1(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request):
        print(request.user.id)
        serializer=CartSer1(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'success':"cart added successfully",'data':serializer.data},status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
