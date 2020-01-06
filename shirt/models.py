from django.db import models

# Create your models here.


class StyleShirt(models.Model):
	name = models.CharField(max_length=200)
	image = models.FileField(upload_to='styles/')
	image_ckpt = models.FileField(upload_to='styles/')
	def __str__(self):
		return self.name

class CompleteShirt(models.Model):
	content = models.FileField(upload_to='content/')
	style = models.ForeignKey('StyleShirt', on_delete=models.CASCADE)