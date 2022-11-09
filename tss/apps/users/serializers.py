#序列化
from rest_framework import serializers
from apps.users.models import UserCustomer,UserCompany,Products,Carts,Orders,OrderDtails

class CreateUserCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    first_name = serializers.CharField(max_length=200,error_messages={ "blank":"first name is required", "max_length":"xxx" })
    last_name = serializers.CharField(max_length=200,error_messages={ "blank":"first name is required", "max_length":"xxx" })
    def validate(self, attrs):
        email = attrs.get("email")
        if UserCustomer.objects.filter(email=email).exists():
            raise serializers.ValidationError("User email exists")
        return attrs
class UserCustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomer #绑定哪一个模型
        fields = "__all__" #解析哪些字段

class CreateUserCompanySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    name = serializers.CharField(max_length=200,error_messages={ "blank":"first name is required", "max_length":"xxx" })
    def validate(self, attrs): #前置校验，减小数据库的压力
        email = attrs.get("email")
        if UserCompany.objects.filter(email=email).exists():
            raise serializers.ValidationError("User email exists")
        return attrs
class UserCompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany #绑定哪一个模型
        fields = "__all__" #解析哪些字段

class CreateProductsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200,error_messages={ "blank":"first name is required", "max_length":"xxx" })
    user = serializers.CharField(max_length=200)
    def validate(self, attrs):
        user_id = attrs.get("user")
        if not UserCompany.objects.filter(pk=user_id).exists():
            raise serializers.ValidationError("user dose not exists")
        # SKU = attrs.get("SKU")
        # if Products.objects.filter(SKU=SKU).exists():
        #     raise serializers.ValidationError("SKU exists")
        return attrs
class ProductsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class CartsModelSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_company = serializers.CharField(source='product.user')
    class Meta:
        model = Carts
        exclude = ['id','user','product']