from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    name         = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, unique=True)
    point        = models.IntegerField(default=0)
    coupons      = models.ManyToManyField('Coupon', through='UserCoupon')
    address      = models.CharField(max_length=300, null=True) 
    zip_code     = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "users"

class Address(models.Model):
    zip_code     = models.CharField(max_length=20)

    class Meta:
        db_table = "addresses"

class Coupon(models.Model):
    SIGNUP = 3

    name  = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        db_table = 'coupons'

class UserCoupon(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_coupons'