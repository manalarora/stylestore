from django.urls import path
from . import views


app_name = 'shirt'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("testing/", views.testing, name = "testing"),
]