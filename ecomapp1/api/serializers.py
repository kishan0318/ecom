from rest_framework.serializers import *
from ..models import *
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginSer(Serializer):
    email=EmailField(error_messages={'required':'Email key is required','blank':'Email is required'})
    password=CharField(error_messages={'required':'Password key is required','blank':'Password is required'})
    token=CharField(read_only=True, required=False)

    def validate(self,data):
        qs=User.objects.filter(email=data.get('email'))
        if not qs.exists():
            raise ValidationError('No account with this email')
        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError('Invalid Password')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data['token']='JWT'+str(token)
        return data


class ProductsSer(ModelSerializer):
    class Meta:
        model = Products
        fields =('title','image')


class ProductsSer1(ModelSerializer):
    title=CharField(error_messages={'required':'title key is required','blank':'title  is required'})
    image=ImageField(error_messages={'required':'image key is required','blank':'image is required'})
    class Meta:
        model = Products
        fields ='__all__'


class ProductsUpSer(Serializer):
    title=CharField(error_messages={'required':"enter a valid username",'blank':'Enter a  username'})
    image=ImageField(error_messages={'required':"Image key is required",'blank':'Image is required '})
    def update(self,instance,validated_data):
        instance.title=validated_data.get('title')
        instance.image=validated_data.get('image')
        instance.save()
        return validated_data


class DelProductsSer(ModelSerializer):
    class Meta:
        model = Products


class ListItemSer(ModelSerializer):
    class Meta:
        model=Items 
        fields ='__all__'


class UpdelitemSer(ModelSerializer):
    class Meta:
        model=Items
        fields =('title','price')


class CartSer(ModelSerializer):
    class Meta:
        model=Cart
        fields ='__all__'


class OrderSer(ModelSerializer):
    class Meta:
        model = Order
        fields='__all__'


class PaymentSer(ModelSerializer):
    class Meta:
        model = Payment
        fields= ['order_id','payment_success']


class CartSer1(Serializer):
    #user=CharField(max_length=255)
    items=CharField(max_length=255)
    quantity=IntegerField(default=1)
    def create(self,validated_data):
        obj=Cart.objects.create(user=self.context.get('user'),quantity=validated_data.get('quantity'),items=Items.objects.get(title=validated_data.get('items')))
        obj.save()
        return validated_data






    