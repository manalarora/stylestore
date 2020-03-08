from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('display/', views.displayTemplates, name='display'),

    path('api/add-remove-cart', views.addRemoveCart)
]

