from django import forms
from .models import CompleteShirt

class ShirtForm(forms.ModelForm):
	class Meta:
		model = CompleteShirt
		fields = "__all__"


