from django.db import models

from django.conf import settings

# Create your models here.


class Address(models.Model):
    line_1 = models.CharField(max_length = 50)
    line_2 = models.CharField(max_length = 50)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    pin_code = models.CharField(max_length = 10)
    def __str__(self):
        return self.line_1

class Coupon(models.Model):
    name = models.CharField(max_length = 6)
    valid_from = models.DateTimeField(auto_now_add = True)
    valid_to = models.DateTimeField(auto_now_add = True)
    discount_percentage = models.FloatField()

class Styles(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    image_model = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Templates(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    unit_price = models.FloatField()

    def __str__(self):
        return self.name

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique = True)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 15, null = True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    GENDERS = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('u', 'Undisclosed'),
    )
    gender = models.CharField(max_length = 1, choices = GENDERS, null = True)

    def __str__(self):
        return self.username

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    coupon_used = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    discount = models.FloatField()
    PAYMENT_TYPES = (
        ('c', 'Cash on delivery'),
        ('d', 'Debit Card'),
        ('p', 'PayTM'),
    )
    payment_type = models.CharField(max_length = 1, choices = PAYMENT_TYPES)
    payment_status = models.BooleanField()

    ordered_at = models.DateTimeField(auto_now_add = True)
    expected_delivery = models.DateTimeField()
    delivered_at = models.DateTimeField()

    def __str__(self):
        return self.id

class CompleteDesign(models.Model):
    content_image = models.URLField()
    style = models.ForeignKey(Styles, on_delete=models.CASCADE)
    result_design = models.URLField()

    # storing python list as a string
    styled_templates = models.TextField()

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_purchased = models.BooleanField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True, blank = True)

    complete_design = models.ForeignKey(CompleteDesign, on_delete=models.CASCADE)

    template = models.ForeignKey(Templates, on_delete=models.CASCADE)
    styled_template_url = models.URLField()

    quantity = models.IntegerField()
    unit_price = models.FloatField()
    added_at = models.DateTimeField(auto_now_add = True)
    last_updated_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.id
