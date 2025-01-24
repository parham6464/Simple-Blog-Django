from mimetypes import init
from django import forms 
from allauth.account.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm , UserChangeForm 
from django.contrib.auth.forms import AuthenticationForm
from typing import Any
from django.contrib.auth import get_user_model
from .models import CustomUser

from accounts.models import CustomUser


class CustomCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields = '__all__'


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

###<input name='username' type="text" placeholder="نام کاربری را وارد کنید">
# class MyCustomLoginForm(AuthenticationForm):
#     def __init__(self, request: Any = ..., *args: Any, **kwargs: Any):
#         super().__init__(request, *args, **kwargs)
#         self.fields['username'].widget.attrs.update({
#             'required':True,
#             'name':'username',
#             'type':'text',
#             'id':'username',
#             'placeholder':'نام کاربری را وارد کنید',

#         })
#         self.fields['password'].widget.attrs.update({
#             'required':True,
#             'name':'password',
#             'type':'text',
#             'id':'password',
#             'placeholder':'رمز عبور را وارد کنید',

#         })
#     class Meta:
#         model = get_user_model()
#         fields = ( 'username' , 'password' )


###
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput , max_length=255)

class UserSignUpForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput , max_length=255)
    email = forms.EmailField()
    phone_number = forms.IntegerField()


class UpdateProfile(forms.Form):       
    username = forms.CharField(max_length=255,required=False)
    email = forms.EmailField(required=False , max_length = 200)
    last_name= forms.CharField(max_length=255,required=False)
    first_name = forms.CharField(max_length=255,required=False)
    phone_number =forms.IntegerField(required=False)


class UpdatePasswordProfile(forms.Form):
    current_pass = forms.CharField(max_length=255,required=False)
    new_pass = forms.CharField(max_length=255,required=False)


class ForgetPassowrd (forms.Form):
    email = forms.EmailField(max_length=55 , label='ایمیل')