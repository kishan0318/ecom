from unicodedata import category
from rest_framework.serializers import *
from ..models import *


class SignupSer(Serializer):
    password=CharField(write_only=True,error_messages={'required':'password key is required','blank':'password  is required'})
    email=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    username=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    first_name=CharField(error_messages={'required':False,'blank':True})
    last_name=CharField(error_messages={'required':False,'blank':True})

    def validate(self,data):
        username=data.get('username')
        qs=User.objects.filter(username=data.get('username')).first()
        if qs:
            raise ValidationError("Username already exists")
        
        qs=User.objects.filter(email=data.get('email')).first()
        if qs:
            raise ValidationError("Email already exists")
        return data

    def create(self,validated_data):
        obj=User.objects.create_user(username=validated_data.get('username'),email=validated_data.get('email'),first_name=validated_data.get('first_name'),last_name=validated_data.get('last_name'),is_superuser=True,is_staff=True)
        obj.set_password(validated_data.get('password'))
        obj.save()
        return validated_data


# class ProductsSer(ModelSerializer):
#     class Meta:
#         model = Products
#         fields =('id','title','image')


class ProductsSerializer(ModelSerializer):
    title=CharField(error_messages={'required':'title key is required','blank':'title  is required'})
    image=ImageField(error_messages={'required':'image key is required','blank':'image is required'})
    item_details=SerializerMethodField()

    def get_item_details(self,obj):
        try:
            return Items.objects.filter(products=obj.id).values('id','title','price')
        except:
            return ''

    class Meta:
        model = Products
        fields ='__all__'


#if user want to update any all data or any single data 
class ProductsUpSer(Serializer):
    title=CharField(required=False)
    image=ImageField(required=False)
    def update(self,instance,validated_data):
        title=validated_data.get('title',instance.title)
        image=validated_data.get('image',instance.image)
        instance.save()
        qs=Products.objects.get(id=instance.id)
        qs.title=title
        qs.image=image
        qs.save()
        return validated_data
    

class DelProductsSer(ModelSerializer):
    class Meta:
        model = Products
        fields=('__all__')



class ListItemSer(ModelSerializer):
    category_name=SerializerMethodField()

    def get_category_name(self,obj):
        try:
            return obj.products.title
        except:return " "

    class Meta:
        model=Items 
        exclude=['products']



class ItemCreateSerializer(ModelSerializer):
    class Meta:
        model=Items     
        fields ='__all__'   



class UpdelitemSer(Serializer):
    title=CharField(required=False)
    price=CharField(required=False)
    about=CharField(required=False)
    file=FileField(required=False)
    
    def update(self,instance,validated_data):
        title=validated_data.get('title',instance.title)
        price=validated_data.get('price',instance.price)
        about=validated_data.get('about',instance.about)
        file=validated_data.get('file',instance.file)
        instance.save()
        qs=Items.objects.get(id=instance.id)
        qs.title=title
        qs.price=price
        qs.about=about
        qs.file=file
        qs.save()
        return validated_data
       




    