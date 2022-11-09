from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group
from django.contrib import admin
from apps.users.models import UserCustomer, UserCompany, Products, Carts, Orders, OrderDtails, OrderCompany

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(UserCustomer)
class UserCustomerAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','first_name','last_name','email','phone','age','gender','address'] #列表页

@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','name','email','phone','address','resume'] #列表页

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','name','price','number','user','SKU','image','type','categories','visible','description'] #列表页

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','product','number','total_price','user'] #列表页

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','user','all_money','payment'] #列表页

@admin.register(OrderDtails)
class OrderDtailsAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['order','product','number','total_money'] #列表页

@admin.register(OrderCompany)
class OrderCompanyAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['order','orderdetail','company'] #列表页