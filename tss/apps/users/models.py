from enum import IntEnum

from django.db.migrations.utils import COMPILED_REGEX_TYPE

from apps.utils.base_model import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UserGender(IntEnum):
    FEMAIL,MAIL,UNKONWN = 0,1,2

    @classmethod
    def choices(cls):
        return tuple(((item.value,item.name) for item in cls))

class ProductType(IntEnum):
    DIGITAL,PHYSICAL = 0,1

    @classmethod
    def choices(cls):
        return tuple(((item.value,item.name) for item in cls))

class OrderStatus(IntEnum):
    AWAITING_PAYMENT = 0 #等待顾客付款
    AWAITING_CHECK = 1 #付款成功后，等待店主确认
    AWAITING_SHIPPING = 2 #店主确认后等待店主发货
    SHIPPING = 3 #运输中
    SHIPPED = 4 #货物已到达
    CUSTOMER_CHECK = 5 #用户签收
    COMPILED = 6 #订单完成
    CANCEL = 7 #取消订单

    @classmethod
    def choices(cls):
        return tuple(((item.value,item.name) for item in cls))

class OrderPayment(IntEnum):
    CHECKOUT = 0 #直接确认
    INSTORE = 1 #线下商店付款
    CARD = 2 #银行卡
    APP = 3 #支付软件

    @classmethod
    def choices(cls):
        return tuple(((item.value,item.name) for item in cls))

class UserCustomer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age = models.SmallIntegerField(validators=[ MinValueValidator(0), MaxValueValidator(200)],default=0)
    address = models.CharField(max_length=200,default="unkown address")
    gender = models.SmallIntegerField(choices=UserGender.choices(),default=2)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        db_table = 'user_customer'
        verbose_name = 'user_customer'
        verbose_name_plural = 'user_customer'

class UserCompany(models.Model):
    name = models.CharField(max_length=200,unique=True)
    email = models.EmailField(max_length=200,unique=True)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200,default="unkown adress")
    resume = models.TextField(max_length=200,default="this is resume")

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        db_table = 'user_company'
        verbose_name = 'user_company'
        verbose_name_plural = 'user_company'

class Products(models.Model):
    user = models.ForeignKey(UserCompany,related_name='company_products',on_delete=models.CASCADE)
    SKU = models.CharField(max_length=200,unique=True,default="unkown sku")
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200,default="unkown image")
    type  = models.SmallIntegerField(choices=ProductType.choices(),default=0)
    categories = models.CharField(max_length=200,default="unkown categories")
    price = models.CharField(max_length=200,default=0)
    number = models.CharField(max_length=200,default=1)
    visible = models.BooleanField(default=True) #1 可见 0 不可见
    description = models.TextField(default="this is a description")

    class Meta:
        db_table = 'products'

class Carts(models.Model):
    user = models.ForeignKey(UserCustomer,related_name='customer_carts',on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='products_carts',on_delete=models.CASCADE)
    total_price = models.CharField(max_length=200,default=0)

    class Meta:
        db_table = 'carts'

class Orders(models.Model):
    customer = models.ForeignKey(UserCustomer,related_name='customer_orders',on_delete=models.CASCADE)
    company = models.ForeignKey(UserCompany,related_name='company_orders',on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=OrderStatus.choices(),default=0)
    number = models.CharField(max_length=200,default=1)
    money = models.CharField(max_length=200,default=1)
    payment = models.SmallIntegerField(choices=OrderPayment.choices(),default=0)

    class Meta:
        db_table = 'orders'
