from django import forms
from main import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget = forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model = models.CustomUser
        exclude = ('address', )

class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'

