from django import forms

# Create your forms here.

from main import models

class CreateStyledImageForm(forms.Form):
    content_image = forms.FileField()
    style = forms.CharField()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model = models.CustomUser
        fields = '__all__'

