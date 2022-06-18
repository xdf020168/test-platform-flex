#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:urls
@time:2022/06/18
@email:tao.xu2008@outlook.com
@description:
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.user_auth.views import MyTokenObtainPairView, LogoutAPIView, UserProfileViewSet
from applications.user_auth.ldap_auth import LoginAuth, LogoutAuth, CheckLogin


router = DefaultRouter()

router.register(r'jwt/user/info', UserProfileViewSet, basename='retrieve'),
router.register(r'jwt/user/list', UserProfileViewSet, basename='list'),
router.register(r'jwt/user/add', UserProfileViewSet, basename='create'),
router.register(r'jwt/user/update', UserProfileViewSet, basename='update'),
router.register(r'jwt/user/del', UserProfileViewSet, basename='destroy')


urlpatterns = [
    path('', include(router.urls)),
    path('jwt/user/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/user/logout', LogoutAPIView.as_view(), name='logout'),

    path('ldap/user/login', LoginAuth.as_view(), name='ldap_login'),
    path('ldap/user/logout', LogoutAuth.as_view(), name='ldap_logout'),
    path('ldap/user/check_login', CheckLogin.as_view(), name='ldap_check'),
]


if __name__ == '__main__':
    pass
