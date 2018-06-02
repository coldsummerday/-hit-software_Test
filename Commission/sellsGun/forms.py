# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class RegForm(UserCreationForm):
    '''
    注册表单

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})
    aliasName = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "昵称", "required": "required",}),
                              max_length=50,error_messages={"required": "昵称不能为空",})
    userType = forms.ChoiceField(choices=(('employee',"销售员"),("boss","老板")))
    '''
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email","userType","aliasName")




