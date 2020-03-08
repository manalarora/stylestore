from django.contrib import admin

from main import models

# Register your models here.
admin.site.register([
    models.Address,
    models.Coupon,
    models.Styles,
    models.Templates,
    models.CustomUser,
    models.Order,
    models.CompleteDesign,
    models.Cart,
])
