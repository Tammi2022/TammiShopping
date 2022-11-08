from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from apps.users.models import UserCustomer,UserCompany
from django.conf import settings

class JWTAuthentication(BaseAuthentication):

    def authenticate(self,request):
        auth_token = request.META.get("HTTP_AUTHTOKEN","")
        try:
            payload = jwt.decode(auth_token,settings.SECRET_KEY,algorithms=['HS256']) #解析token
        except (jwt.DecodeError,jwt.InvalidSignatureError):
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        email = payload.get("email")
        user = UserCustomer.objects.filter(email=email).first()
        if not user:
            user = UserCompany.objects.filter(email=email).first()
            if not user:
                raise exceptions.AuthenticationFailed('Unauthenticated')
        return user,None