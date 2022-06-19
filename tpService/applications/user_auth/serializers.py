#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:serializers
@time:2022/06/18
@email:tao.xu2008@outlook.com
@description:
"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from applications.user_auth.models import UserProfile
from commons.drf_base import JsonResponse


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'  # ('name', 'permissions')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'  # ('id', 'username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    扩展用户 信息序列化
    """
    user = UserSerializer()
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_name(self, obj):
        return obj.user.username


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, UserSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['roles'] = [g.name for g in Group.objects.filter(user=user.id)]
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['token'] = data.get('access')
        # custom_data = {'token': data.get('access')}
        return JsonResponse(data, msg='success!').data


if __name__ == '__main__':
    pass
