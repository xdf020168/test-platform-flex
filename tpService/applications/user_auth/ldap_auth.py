#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:ldap_auth
@time:2022/06/18
@email:tao.xu2008@outlook.com
@description:
"""
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from commons.drf_base import JsonResponse

logger = logging.getLogger()


class LoginAuth(APIView):
    """登录"""
    def post(self, request):
        user_loggedin = 'Guest'
        display_name = "Guest"
        context = {'username': user_loggedin, 'displayName': display_name, 'state': False}
        data = request.data
        username = data.get('username')
        password = data.get('password')
        usergo = authenticate(username=username, password=password)
        logger.info(usergo)
        if usergo is not None:
            login(request, usergo)
            # uu = request.user
            user_loggedin = usergo.username
            display_name = usergo.first_name
            context = {'username': user_loggedin, 'displayName': display_name, 'state': True}

        return JsonResponse(data=context, status=status.HTTP_200_OK)


class LogoutAuth(APIView):
    """登出"""
    def post(self, request):
        logout(request)
        return JsonResponse(data={'message': 'logout success!', }, status=status.HTTP_200_OK)


class CheckLogin(APIView):
    """登录检查"""
    def get(self, request):
        user_loggedin = 'Guest'
        display_name = "Guest"
        context = {'username': user_loggedin, 'displayName': display_name, 'state': False}
        uu = request.user
        if uu:
            usergo = User.objects.filter(username=uu).first()
            if usergo is not None:
                user_loggedin = usergo.username
                display_name = usergo.first_name
                context = {'username': user_loggedin, 'displayName': display_name, 'state': True}
        return JsonResponse(data=context, status=status.HTTP_200_OK)


if __name__ == '__main__':
    pass
