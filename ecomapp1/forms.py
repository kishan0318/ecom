from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from django.forms.widgets import Widget
from django.contrib.auth import authenticate

class Register(forms.ModelForm):
    address=forms.CharField(max_length=1000,required=True,help_text="Please fill your address correctly.",error_messages={'required':'Please fill your address correctly','blank':'address field is mandatory'})
    password=forms.CharField(widget=forms.PasswordInput)
    retype_password=forms.CharField(widget=forms.PasswordInput)
    mobile=forms.CharField(max_length=11,required=True,help_text="Please fill your mobile no. correctly.",error_messages={'required':'Please fill your mobile no. correctly','blank':'mobile field is mandatory'})
    class Meta:
        model=User
        fields=['username',"first_name","last_name","email"]
    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get("retype_password")
        if p!=p1:
            raise forms.ValidationError("both passwords didnot math")

class Logform(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data.get('username')
        p=self.cleaned_data.get('password')
        ur=authenticate(username=u,password=p)
        if ur==None:
            raise ValidationError("user does not exists")
       

