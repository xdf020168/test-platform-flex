#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:rf_base
@time:2022/06/18
@email:tao.xu2008@outlook.com
@description:
"""

from collections import OrderedDict
import six
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny


# 定制统一的接口请求返回数据格式
class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=20000, msg='ok', success='true',
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)
        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        self.data = {"code": code, "msg": msg, "success": success, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


# 定制化分页
class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('list', data)
        ]))

    page_query_param = 'page'  # 页码--参数名称
    page_size_query_param = 'page_size'  # 每页多少条--参数名称
    page_size = 20
    max_page_size = 10000


# DRF ViewSet封装
class BaseViewSet(ModelViewSet):
    # 登录认证
    # permission_classes = [IsAuthenticated, ]
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = Pagination  # 分页

    # 创建数据
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 检索数据
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 更新数据
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 部分更新数据
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 删除数据
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(response.data, status=200)

    # 查询数据
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)


if __name__ == '__main__':
    pass
