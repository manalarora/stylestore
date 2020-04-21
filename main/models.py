from django.db import models

from django.conf import settings

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    line_1 = models.CharField(max_length = 50)
    line_2 = models.CharField(max_length = 50)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    pin_code = models.CharField(max_length = 10)

    is_shipping = models.BooleanField(default = False)
    is_billing = models.BooleanField(default = False)

    def __str__(self):
        return self.line_1
    
    class Meta:
        verbose_name_plural = "addresses"

class Coupon(models.Model):
    name = models.CharField(max_length = 6)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_valid = models.BooleanField(default = True)
    discount_percentage = models.FloatField()
    
    class Meta:
        verbose_name_plural = "coupons"

class Styles(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    image_model = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "styles"

class Templates(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    unit_price = models.FloatField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "templates"

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique = True)
    phone_number = models.CharField(max_length = 15, null = True)
    GENDERS = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('u', 'Undisclosed'),
    )
    gender = models.CharField(max_length = 1, choices = GENDERS, null = True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "CustomUsers"

class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    coupon_used = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    discount = models.FloatField()
    PAYMENT_TYPES = (
        ('c', 'Cash on delivery'),
        ('d', 'Debit Card'),
        ('p', 'PayTM'),
    )
    payment_type = models.CharField(max_length = 1, choices = PAYMENT_TYPES)
    payment_status = models.BooleanField()

    ordered_at = models.DateTimeField()
    expected_delivery = models.DateTimeField()
    delivered_at = models.DateTimeField()

    shipping_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name = 'shipping_address_set')
    billing_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name = 'billing_address_set')
    class Meta:
        verbose_name_plural = "orders"

class CompleteDesign(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    is_public = models.BooleanField(default = True)

    content_image = models.URLField()
    style = models.ForeignKey('Styles', on_delete=models.CASCADE)
    result_design = models.URLField()

    # storing python list as a string
    styled_templates = models.TextField()
    
    class Meta:
        verbose_name_plural = "CompleteDesigns"

class Cart(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    is_purchased = models.BooleanField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null = True, blank = True)

    complete_design = models.ForeignKey('CompleteDesign', on_delete=models.CASCADE)

    template = models.ForeignKey('Templates', on_delete=models.CASCADE)
    styled_template_url = models.URLField()

    quantity = models.IntegerField()
    unit_price = models.FloatField()

    added_at = models.DateTimeField()
    last_updated_at = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = "cart"
