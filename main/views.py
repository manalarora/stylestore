from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from keras.preprocessing.image import save_img
import numpy as np
tf.compat.v1.enable_eager_execution()

from django.conf import settings

from main import models as main_models
from main import forms as main_forms

import cloudinary
import requests
import io
from PIL import Image

cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET")
)

def load_img(path_to_img):
    # img = tf.io.read_file(path_to_img)
    img = requests.get(path_to_img).content
    img = tf.image.decode_jpeg(img, channels=3)
    # the following line will convert the image to float value ie between 0 and 1
    img = tf.image.convert_image_dtype(img, tf.float32)
    # the following line will resize the image to 256,256
    img = tf.image.resize(img, (256, 256))
    # the following line will add a new axis to the image
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    print("aa")
    tensor = tensor*255
    print("aa")
    tensor = np.array(tensor.numpy(), dtype=np.uint8)
    print("aa")
    if np.ndim(tensor)>3:
        print("aa")
        assert tensor.shape[0] == 1
        print("aa")
        tensor = tensor[0]
    print("aa")
    return tensor

# from main.functions.functions import handle_uploaded_file
# Create your views here.
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), padding='same', input_shape=(256, 256, 3)))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(128, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(layers.Conv2D(256, (3, 3), padding='same'))
# model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones'))#, beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
# model.add(Activation('relu'))
# model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(256, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2DTranspose(128, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2DTranspose(64, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2DTranspose(32, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(3, (3, 3), activation='tanh', padding='same'))

def uploadImage(image, path):
    # https://cloudinary.com/documentation/django_integration
    # cloudinary.uploader.upload("dog.mp4", 
    # folder = "my_folder/my_sub_folder/", 
    # public_id = "my_dog",
    # overwrite = true, 
    # notification_url = "https://mysite.example.com/notify_endpoint", 
    # resource_type = "video")
    
    # upload image to cloud
    # cloudinary.uploader.upload(request.FILES['file'])
    print("bb")
    uploaded_image = cloudinary.uploader.upload(image,
        folder = path,
        overwrite = True,
        resource_type = "image"
    )
    print("bb")
    image_url = uploaded_image["secure_url"]
    # image_url = uploaded_image["url"]
    print("bb")
    print(image_url)
    return image_url

def index(request):
    if request.session.get('checkout_active', False):
        return HttpResponseRedirect('/checkout')
    
    if request.method == "POST":
        form = main_forms.CreateStyledImageForm(request.POST, request.FILES)
        if form.is_valid():
            style_id = form.cleaned_data['style']
            content_image_url = uploadImage(form.cleaned_data['content_image'], settings.DATA["CONTENT_IMAGE_CLOUD"])

            temp = main_models.Styles.objects.get(id = style_id)
            # now we have somehow form the final image
            # temp = CompleteShirt.objects.latest('id')
            # model.load_weights(temp.style.image_ckpt.url[1:])

            print("lol1")
            model.load_weights(settings.DATA["STYLES_IMAGE_MODEL"] + temp.image_model)
            print("lol2")

            image = load_img(content_image_url)
            print("lol3")
            image = model(image)
            print("lol4")
            image = (image+1)/2
            print("lol5")
            image = tensor_to_image(image)
            print("lol6")
            # saving result image at result_image_url path
            # out_img = Image.fromarray(image).convert('RGB')
            # result_image = io.BytesIO()
            # out_img.save(result_image, format='png')
            # result_image.seek(0)
            # result_image_url = uploadImage(result_image, settings.DATA["RESULT_IMAGE_CLOUD"])
            # ==================================
            result_image_url = settings.DATA["RESULT_IMAGE"]
            save_img(result_image_url, image)
            result_image_url = "/" + result_image_url
            os.system("python manage.py collectstatic --no-input")
            print("lol7")

            # os.system(". tf/bin/activate")
            # os.system("python3 fast-style-transfer-master/evaluate.py --checkpoint "+temp.style.image_ckpt.url[1:]+" --in-path "+temp.content.url[1:]+" --out-path media/images/123.jpg")

            request.session['style'] = style_id
            request.session['content_image'] = content_image_url
            request.session['result_image'] = result_image_url
            return HttpResponseRedirect('/checkout')
    context = {
        "styleshirts": main_models.Styles.objects.all
    }
    return render(request, 'main/home.html', context)

def checkout(request):
    request.session['checkout_active'] = True
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/auth/login')
    if not request.session.get('style', None):
        return HttpResponseRedirect('/auth/login')
    if not request.session.get('content_image', None):
        return HttpResponseRedirect('/auth/login')
    if not request.session.get('result_image', None):
        return HttpResponseRedirect('/auth/login')
    
    
    context = {
        "content_image": request.session['content_image'],
        "result_image": request.session['result_image'],
        "templates": main_models.Templates.objects.all
    }

    if request.session.get('checkout_active', False):
        del request.session['checkout_active']
    
    return render(request, 'main/display.html', context)



