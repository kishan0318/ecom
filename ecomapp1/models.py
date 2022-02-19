from re import S, U
from turtle import mode
from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.contrib.auth.models import User

class Products(models.Model):
    title=models.CharField(max_length=100,help_text='Cateogry title')
    image=models.ImageField(upload_to="Product_image")
    class Meta:
        verbose_name_plural="Cateogries"
    def __str__(self): 
        return f"Cateogries Name:{self.title}"
    def get_absolute_url(self):
        return reverse('ecomapp1:home')

class Items(models.Model):
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    price=models.CharField(max_length=50)
    about=models.CharField(max_length=300)
    file=models.ImageField(upload_to='items_images')
    class Meta:
        verbose_name_plural="Products"

    def __str__(self):
        return f"Item Name:{self.title} "
    def get_absolute_url(self):
        return reverse('ecomapp1:items',kwargs={'pk':self.al_id.id})

'''class Profile(models.Model):     
    u_id=models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'], 'allowed:images')])
    address= models.TextField()
    dob=models.DateField()
    def get_absolute_url(self):
        return reverse('ecomapp1:profile',kwargs={'pk':self.u_id.id})'''

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"USERNAME: {self.user.username}--------items: {self.items.title}"

TITLE_CHOICES = [
    ('1', 'success'),
    ('2','pending'),
    ('3', 'processing'),
]

class Order(models.Model):
    item=models.ForeignKey(Items, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    shipping_address=models.CharField(max_length=225,null=True)
    Is_payment_success=models.CharField(max_length=10,choices=TITLE_CHOICES,default='2')
   # date=models.DateField()
    def __str__(self):
        return f"Order_id:{str(self.id)}"

class Payment(models.Model):
    order_id=models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_success= models.BooleanField(default=False)
    def __str__(self):
        return f"payments:{self.order_id}"




    
   
