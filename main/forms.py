from django import forms

# Create your forms here.

from main import models

class CreateStyledImageForm(forms.Form):
    content_image = forms.FileField()
    style = forms.CharField()

