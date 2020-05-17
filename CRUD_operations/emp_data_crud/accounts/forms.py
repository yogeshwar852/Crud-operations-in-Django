from django import forms
from django.contrib.auth import get_user_model
from .models import EmpInfo
from django.forms import ModelForm


User = get_user_model()

class OrderForm(ModelForm):
    class Meta:
        model = EmpInfo
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password_first = forms.CharField(min_length=6,required=True, label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(min_length=6,required=True, label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        password_one = self.cleaned_data.get('password_first')
        password_two = self.cleaned_data.get('password_again')
        if password_one and password_two and password_one != password_two:
            raise forms.ValidationError("passwords din't match")

        return cleaned_data


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('username already exists')
        return username

    def clean_email(self):
        email_address = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email_address)
        if qs.exists():
            raise forms.ValidationError("this email_id already registered")
        return email_address

    # def clean_password(self):
    #     password_one = self.cleaned_data.get('password_first')
    #     try:
    #         match = User.objects.get(password_first=password_one)
    #     except match.DoesNotExist:
    #         # Unable to find a user, this is fine
    #         return password_one
    #     raise forms.ValidationError("cannot use this password")


    # def clean_password(self):
    #     password_two = self.cleaned_data.get('password_two')
    #     qs = User.objects.filter(password=password_two)
    #     if qs.exists():
    #         raise forms.ValidationError("cannot use this password")
    #     return password_two