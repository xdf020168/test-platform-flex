#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:urls
@time:2022/06/18
@email:tao.xu2008@outlook.com
@description:
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from applications.user_auth.views import MyTokenObtainPairView, TokenDecodeAPIView, \
    LogoutAPIView, UserProfileViewSet
# from applications.user_auth.ldap_auth import LoginAuth, LogoutAuth, CheckLogin


router = DefaultRouter()

# user拓展 - 增删改查
router.register(r'jwt/user/info', UserProfileViewSet, basename='retrieve'),
router.register(r'jwt/user/list', UserProfileViewSet, basename='list'),
router.register(r'jwt/user/add', UserProfileViewSet, basename='create'),
router.register(r'jwt/user/update', UserProfileViewSet, basename='update'),
router.register(r'jwt/user/del', UserProfileViewSet, basename='destroy')


urlpatterns = [
    path('', include(router.urls)),

    # JWT 认证 --默认
    path('jwt/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取JWT token
    path('jwt/token/v2', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取JWT token，自定义
    path('jwt/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新JWT token
    path('jwt/token/info', TokenDecodeAPIView.as_view(), name='token_info'),  # JWT token payload

    # JWT 认证 --拓展
    path('jwt/user/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/user/logout', LogoutAPIView.as_view(), name='logout'),

    # ldap
    # path('ldap/user/login', LoginAuth.as_view(), name='ldap_login'),
    # path('ldap/user/logout', LogoutAuth.as_view(), name='ldap_logout'),
    # path('ldap/user/check_login', CheckLogin.as_view(), name='ldap_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if __name__ == '__main__':
    pass
