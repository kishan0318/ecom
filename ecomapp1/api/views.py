from functools import partial
from importlib.metadata import requires
from itertools import product
from urllib import request
from django.shortcuts import render
from rest_framework import generics,serializers
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from ..models import Products,Items
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

class SignupAPIView(APIView):
    permission_classes =[AllowAny,]

    def post(self,request):
        serializer=SignupSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({'Success':'user created successfully','data':data},status=HTTP_200_OK)
        return Response({'message':serializer.errors
        },status=HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    permission_classes = (AllowAny)

    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        if not user:
            returnMessage = {'error': 'Invalid Credentials'}
            return Response(returnMessage,status=HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        token.save()
        returnToken = {'token':token.key,'username':user.username}
        return Response(returnToken,status=HTTP_200_OK)




#any user can view the products(Cateogries)
class ProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer



#only admin user can view and create products(Cateogries)
class ProductCreateApi(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser,]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer



#only admin user can update products
class ProductsUpAPIView(APIView):
    permission_classes =[IsAdminUser,]
    # queryset = Products.objects.all()
    # serializer_class=ProductsUpSer
    def put(self,request,*args,**kwargs):
        qs=Products.objects.filter(id=self.kwargs['pk']).first()
        serializer=ProductsUpSer(qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Updated successfully','data':serializer.data},200)
        return Response({'message':serializer.errors},400)



#admin user can delete 
class DeleteProductsAPIView(APIView):
    permission_classes =[IsAdminUser,]
    def delete(self,request,*args,**kwargs):
        try:
            qs= Products.objects.filter(id=self.kwargs['pk'])
            qs.delete()
            return Response({'message':'Deleated successfully!'},200)
        except:return Response({'message':'Deleated successfully!'},400)
        


#anyone can view items
# class ItemsAPIView(generics.ListAPIView):
#     permission_classes=[AllowAny,]
#     queryset=Items.objects.all()
#     serializer_class=ListItemSer

#only admin can create items
class ItemsAPIView(generics.ListAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Items.objects.all()
    serializer_class=ListItemSer


class ItemsCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Items.objects.all()
    serializer_class=ItemCreateSerializer


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
