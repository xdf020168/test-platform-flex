#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:ldap_auth
@time:2022/02/07
@email:tao.xu2008@outlook.com
@description: JWT
"""
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from applications.user_auth.serializers import MyTokenObtainPairSerializer
from commons.drf_base import BaseViewSet, JsonResponse
from applications.user_auth.models import UserProfile
from applications.user_auth.serializers import UserProfileSerializer


User = get_user_model()


# JWT认证
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# 支持邮箱登录认证
class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class TokenDecodeAPIView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        token_info = TokenBackend(algorithm='HS256').decode(token, verify=False)
        return JsonResponse(data=token_info)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse(data={'message': 'logout success!', }, status=200)


# 用户扩展类 增删改查
class UserProfileViewSet(BaseViewSet):
    """
    用户扩展类 增删改查
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('id')
