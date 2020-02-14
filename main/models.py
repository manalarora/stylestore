from django.db import models

from django.conf import settings

# Create your models here.

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
    name = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 15, null = True)
    address = models.TextField()
    GENDERS = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('u', 'Undisclosed'),
    )
    gender = models.CharField(max_length = 1, choices = GENDERS, null = True)

    def __str__(self):
        return self.username

class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    content_image = models.URLField()
    style = models.ForeignKey(Styles, on_delete=models.CASCADE)
    styled_image = models.URLField()

    templates = models.ManyToManyField(Templates)

    bill_amount = models.FloatField()
    PAYMENT_TYPES = (
        ('c', 'Cash on delivery'),
        ('d', 'Debit Card'),
        ('p', 'PayTM'),
    )
    payment_type = models.CharField(max_length = 1, choices = PAYMENT_TYPES)
    payment_status = models.BooleanField()

    ordered_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.id

