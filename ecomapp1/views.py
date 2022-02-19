from .models import Products,Items,Cart
from django.views.generic import ListView,DetailView,View,DeleteView,UpdateView,CreateView
from .forms import Register,Logform
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy,reverse


# Create your views here.

class Home(ListView):
    template_name="home.html"
    context_object_name='data'
    def get_queryset(self):
        return {'car':enumerate(Products.objects.all()),'dt':Products.objects.all()}

class Dts(DetailView):
    model=Products
    template_name='Items.html'
    context_object_name='data'
       
class Signup(View):
    def get(self,request):
        f=Register(None)
        return render(request,'signup.html',{"data":f})
    def post(self,request):
        f=Register(request.POST)
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get('password')
            data.set_password(p)
            data.save()
            return redirect('ecomapp1:login')
        return render(request,'signup.html',{"data":f})

class Signin(View):
    def get(self,request):
        f=Logform(None)
        return render(request,'login.html',{"data":f})
    def post(self,request):
        f=Logform(request.POST)
        if f.is_valid():
            u=f.cleaned_data.get("username") 
            p=f.cleaned_data.get("password")
            ur=authenticate(username=u,password=p)
            nxt=request.GET.get('next')
            print(nxt)
            if ur:
                login(request,ur)
                if nxt:
                    return redirect(nxt)
                else:
                    return redirect('ecomapp1:home')
        return render(request,'login.html',{"data":f})


class StaffLogin(View):
    def get(self, request):
        f=Logform(None)
        k={'data':f}
        return render(request,'login.html',k)
    def post(self,request):
        f=Logform(request.POST)
        k={'data':f}
        if f.is_valid():
            u=f.cleaned_data.get('username')
            p=f.cleaned_data.get('password')
            ur=authenticate(username=u,password=p) 
            if ur.is_staff==False:
                return HttpResponse("you cant access this page")
            elif ur.is_staff==True:
                nxt=request.GET.get('next')
            if ur:
                login(request,ur)
                if nxt:
                    return redirect(nxt)
                else:
                     return redirect('ecomapp1:home')
        return render(request,'login.html',k)

class Add_Product(LoginRequiredMixin,CreateView):
    login_url = 'ecomap1:StaffLogin'
    model = Products
    fields = ('__all__')
    template_name = 'addproduct.html' 

class Up_Product(LoginRequiredMixin,UpdateView):
    login_url = 'ecomapp1:StaffLogin'
    model=Products
    fields=('__all__')
    template_name='updateproduct.html'

class Del_product(LoginRequiredMixin,DeleteView):
    login_url = 'ecomapp1:StaffLogin' 
    model=Products 
    success_url=reverse_lazy('ecomapp1:home')
    template_name='deleteproduct.html'
    context_object_name='data'

def signout(request):
    logout(request)
    return redirect("ecomapp1:home")

def about(request):
    return render(request,'aboutus.html')

class AddItem(LoginRequiredMixin,CreateView):
    login_url = 'ecomapp1:StaffLogin'
    model=Items
    fields=('__all__')
    template_name='addproduct.html' 
    def form_valid(self, form):
        p=self.kwargs.get('pk')
        a=Products.objects.get(id=p)
        form.instance.al_id=a 
        return super().form_valid(form)

class DelItem(LoginRequiredMixin,DeleteView):
    login_url = 'ecpmapp1:StaffLogin'
    model=Items
    success_url=reverse_lazy('ecomapp1:home')
    template_name='deleteproduct.html'
    context_object_name='data'

class Dts1(DetailView):
    model=Items
    template_name='detail.html'
    context_object_name='data'
    
def action(request):
    return HttpResponse('Your order placed succesfully')
    
def add_to_cart(request,*args,**kwargs):
    if request.user.is_authenticated:
        user = request.user
        item_ids=kwargs.get('pk')
        #print("hellogdfgnbdhbjgskbshk",item_ids)
        #item_id=request.GET.get('item_id')
        #print("hellogdfgnbdhbjgskbshk",item_id)
        itm= Items.objects.get(id=item_ids)
        Cart(user=user, items=itm).save()
        return redirect('ecomapp1:show_cart')
    return redirect('ecomapp1:login')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart=Cart.objects.filter(user=user)
        return render(request, 'cart.html',{'cart':cart})

class DelCart(LoginRequiredMixin,DeleteView):
    model=Cart
    success_url=reverse_lazy('ecomapp1:show_cart')
    template_name='deletecart.html'
    context_object_name='data'

def payment(request):
    return render(request, 'payment.html')

'''client = razorpay.Client(auth=("rzp_test_md5f7Wpov0K4Vf", "lcbIpGmt3A5qutIPSDoOcdtu"))

def payment(request):
        DATA = {
        "amount": 5000,
        "currency": "INR",
        "receipt": "receipt#1",
        'payment_capture':1,
        "notes": {
        "key1": "value3",
        "key2": "value2"}}
        client.order.create(data=DATA)
        context={'amount':500,}
        return redirect('ecomapp1:show_cart')'''

