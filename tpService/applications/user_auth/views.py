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
from rest_framework_simplejwt.views import TokenObtainPairView

from applications.user_auth.serializers import MyTokenObtainPairSerializer
from commons.drf_base import BaseViewSet, JsonResponse
from applications.user_auth.models import UserProfile
from applications.user_auth.serializers import UserProfileSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse(data={'message': 'logout success!', }, status=200)


class UserProfileViewSet(BaseViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('id')
