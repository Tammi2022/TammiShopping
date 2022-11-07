from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group
from django.contrib import admin
from apps.users.models import UserCustomer,UserCompany

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(UserCustomer)
class UserCustomerAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at'] #展示在详情页，exclude是排除
    list_display = ['id','first_name','last_name','email','gender','age'] #列表页