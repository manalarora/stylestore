from django.shortcuts import render
from django.http import HttpResponse
from .models import StyleShirt, CompleteShirt
from .forms import ShirtForm
import os as os
# from shirt.functions.functions import handle_uploaded_file
# Create your views here.


def homepage(request):
	if request.method == "POST":
		form = ShirtForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# now we have somehow form the final image
			temp = CompleteShirt.objects.latest('id')
			# os.chdir(os.getcwd()+"/../")
			print(os.getcwd())
			# files = os.listdir(os.getcwd())
			# for name in files:
			# 	print(name)
			for (root,dirs,files) in os.walk('', topdown=True): 
				print(root)
				print(dirs)
				print(files)
				print('--------------------------------')
			os.system(". tf/bin/activate")
			os.system("python3 fast-style-transfer-master/evaluate.py --checkpoint "+temp.style.image_ckpt.url[1:]+" --in-path "+temp.content.url[1:]+" --out-path media/images/123.jpg")

			return HttpResponse("File uploaded successfuly")
	return render(request = request,
                  template_name='shirt/home.html',
                  context = {"styleshirts":StyleShirt.objects.all,
                  "form":ShirtForm})

def testing(request):
	if request.method == "POST":
		form = ShirtForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			text = "Saved"
			return HttpResponse("File uploaded successfuly")  
			# post is th name of the variable declared in the form
			# return render(request,
			# 	'shirt/testing.html',
			# 	{"form": ShirtForm,
			# 	"text": text})


	return render(request,
		'shirt/testing.html',
		{"form": ShirtForm})

