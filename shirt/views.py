from django.shortcuts import render
from django.http import HttpResponse
from .models import StyleShirt, CompleteShirt
from .forms import ShirtForm
import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from keras.preprocessing.image import save_img
import numpy as np
tf.compat.v1.enable_eager_execution()




def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_jpeg(img, channels=3)
#   the following line will convert the image to float value ie between 0 and 1
    img = tf.image.convert_image_dtype(img, tf.float32)
#   the following line will resize the image to 256,256
    img = tf.image.resize(img, (256, 256))
#   the following line will add a new axis to the image
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor.numpy(), dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return tensor

# from shirt.functions.functions import handle_uploaded_file
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

def homepage(request):
	if request.method == "POST":
		form = ShirtForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# now we have somehow form the final image
			temp = CompleteShirt.objects.latest('id')
			# model.load_weights(temp.style.image_ckpt.url[1:])

			model.load_weights(temp.style.image_ckpt.url[1:])

			image = load_img(temp.content.url[1:])
			image = model(image)
			image = (image+1)/2
			image = tensor_to_image(image)
			save_img('media/images/123.jpg', image)

			# os.system(". tf/bin/activate")
			# os.system("python3 fast-style-transfer-master/evaluate.py --checkpoint "+temp.style.image_ckpt.url[1:]+" --in-path "+temp.content.url[1:]+" --out-path media/images/123.jpg")

			return HttpResponse("File uploaded successfuly")
	return render(request = request,
				  template_name='shirt/home.html',
				  context = {"styleshirts":StyleShirt.objects.all,
							 "form":ShirtForm})

