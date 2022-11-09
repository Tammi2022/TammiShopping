import jwt,json,time
from django.http import  JsonResponse
from django.conf import settings
from apps.users.models import UserCustomer,UserCompany,Products,Carts
from apps.users.serializers import UserCompanyModelSerializer,UserCustomerModelSerializer,\
    CreateUserCompanySerializer,CreateUserCustomerSerializer,\
    ProductsModelSerializer,CreateProductsSerializer,\
    CartsModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserCustomerView(APIView):
    def get(self,request):
        offset = request.GET.get('offset',0)
        limit = request.GET.get('limit',10)
        users = UserCustomer.objects.all()
        total_count = users.count()
        _users = users[offset:offset+limit]
        user_data = UserCustomerModelSerializer(_users,many=True).data
        res = {
            "code":200,
            "message":"success",
            "data":{
                'list':user_data,
                "pagination":{
                    "offset":offset,
                    "limit":limit,
                    "total_count":total_count
                }
            }
        }
        return Response(res)
    def post(self,request):
        user_data = json.loads(request.body)
        serializer = CreateUserCustomerSerializer(
            data = {
            "email":user_data.get('email'),
            "first_name":user_data.get('first_name'),
            "last_name":user_data.get('last_name'),
            "phone":user_data.get('phone'),
            "password":user_data.get('password'),
        })

        if not serializer.is_valid():
            return  Response(serializer.errors)

        _user = UserCustomer.objects.filter(email=user_data['email']).first()
        if _user:
            return Response({"code":404,"message":"User does exist"})

        user = UserCustomer.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            phone=user_data['phone'],
            password=user_data['password'],
        )
        res = {
            "code":200,
            "message":'success',
            "data":{
                "userId":user.id
            }
        }
        return JsonResponse(res)

class UserCompanyView(APIView):
    def get(self,request):
        offset = request.GET.get('offset',0)
        limit = request.GET.get('limit',10)
        users = UserCompany.objects.all()
        total_count = users.count()
        _users = users[offset:offset+limit]
        user_data = UserCompanyModelSerializer(_users,many=True).data
        res = {
            "code":200,
            "message":"success",
            "data":{
                'list':user_data,
                "pagination":{
                    "offset":offset,
                    "limit":limit,
                    "total_count":total_count
                }
            }
        }
        return Response(res)
    def post(self,request):
        user_data = json.loads(request.body)
        serializer = CreateUserCompanySerializer(
            data = {
            "email":user_data.get('email'),
            "name":user_data.get('name'),
            "phone":user_data.get('phone'),
            "password":user_data.get('password'),
        })

        if not serializer.is_valid():
            return  Response(serializer.errors)

        _user = UserCompany.objects.filter(email=user_data['email']).first()
        if _user:
            return Response({"code":404,"message":"User does exist"})

        user = UserCompany.objects.create(
            name=user_data['name'],
            email=user_data['email'],
            phone=user_data['phone'],
            password=user_data['password'],
        )
        res = {
            "code":200,
            "message":'success',
            "data":{
                "userId":user.id
            }
        }
        return JsonResponse(res)

class UserLoginView(APIView):
    authentication_classes = ()
    def post(self,request):
        data = json.loads(request.body)
        email = data.get('email')
        user = UserCustomer.objects.filter(email=email).first()
        if not user:
            user = UserCompany.objects.filter(email=email).first()
            if not user:
                return Response({
                    "code":404,
                    "msg":"Not Found | User does not exist"
                })
        payload = {
            "email": email,
            "exp":int(time.time())+60*60*24,
        }
        secret_key = settings.SECRET_KEY
        token = jwt.encode(payload,secret_key,algorithm='HS256').decode("utf-8")
        res = {
            'code':200,
            "msg":f"success{user}",
            "data":{
                "token":token
            }
        }
        return Response(res)

class ProductsView(APIView):
    def get(self,request):
        offset = request.GET.get('offset',0)
        limit = request.GET.get('limit',10)
        products = Products.objects.all()
        total_count = products.count()
        _products = products[offset:offset+limit]
        products_data = ProductsModelSerializer(_products,many=True).data
        res = {
            "code":200,
            "message":"success",
            "data":{
                'list':products_data,
                "pagination":{
                    "offset":offset,
                    "limit":limit,
                    "total_count":total_count
                }
            }
        }
        return Response(res)
    def post(self,request):
        product_data = json.loads(request.body)
        serializer = CreateProductsSerializer(
            data = {
            "name":product_data.get('name'),
            "user":product_data.get('user'),
        })

        if not serializer.is_valid():
            return  Response(serializer.errors)

        _user = UserCompany.objects.filter(id=product_data['user']).first()
        if not _user:
            return Response({"code":404,"message":"UserCompany does not exist"})

        product = Products.objects.create(
            name=product_data['name'],
            user=_user,
        )
        res = {
            "code":200,
            "message":'success',
            "data":{
                "productId":product.id
            }
        }
        return JsonResponse(res)

class CompanyProductsView(APIView):
    authentication_classes = ()
    def get(self, request, user_id):
        user = UserCompany.objects.filter(pk=user_id).first()
        if not user:
            res = {
                "code": "404",
                "message": "user not exists"
            }
            return Response(res)
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        company_products = user.company_products.all()
        total_count = company_products.count()
        _products = company_products[offset:offset + limit]
        products_data = ProductsModelSerializer(_products, many=True).data
        res = {
            "code": 200,
            "message": "success",
            "data": {
                'list': products_data,
                "pagination": {
                    "offset": offset,
                    "limit": limit,
                    "total_count": total_count
                }
            }
        }
        return Response(res)

class CustomerCartsView(APIView):
    authentication_classes = ()
    def get(self, request, user_id):
        user = UserCustomer.objects.filter(pk=user_id).first()
        if not user:
            res = { "code": "404","message": "user not exists"}
            return Response(res)
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        customer_carts = Carts.objects.filter(user=user).all()
        total_count = customer_carts.count()
        _carts = customer_carts[offset:offset + limit]
        carts_data = CartsModelSerializer(_carts, many=True).data
        res = {
            "code": 200,
            "message": "success",
            "data": {
                'list': carts_data,
                "pagination": {
                    "offset": offset,
                    "limit": limit,
                    "total_count": total_count
                }
            }
        }
        return Response(res)
    def post(self,request, user_id):
        cart_data = json.loads(request.body)
        user = UserCustomer.objects.filter(pk=user_id).first()
        if not user:
            return Response({"code": "404", "message": "user not exists"})
        product = Products.objects.filter(id=cart_data['product']).first()
        if not product:
            return Response({"code": "404", "message": "product not exists"})
        cart = Carts.objects.create(
            user=user,
            product=product,
            number=cart_data["number"],
            total_price=cart_data["total_price"],
        )
        res = {
            "code":200,
            "message":'success',
            "data":{
                "cartId":cart.id
            }
        }
        return JsonResponse(res)

