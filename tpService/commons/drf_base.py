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
from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_bulk import BulkModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny


# 定制统一的接口请求返回数据格式
class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=2, msg='ok', success='true',
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
class BaseViewSet(BulkModelViewSet):
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

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        response = super().bulk_update(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        response = super().partial_bulk_update(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)

    # 删除数据
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(response.data, status=200)

    # 批量 删除数据执行条件
    def allow_bulk_destroy(self, qs, filtered):
        print(qs.count())
        print(filtered.count())
        return (qs is not filtered) and self.request.query_params and qs.count() > filtered.count()

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        response = super().bulk_destroy(request, *args, **kwargs)
        if response.status_code == 400:
            return JsonResponse(None, msg="筛选参错误/空，禁止全表删除！", code=500500, status=200)
        return JsonResponse(response.data, status=200)

    # 查询数据
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(response.data, status=response.status_code)


class TotalCountModelMixin(GenericViewSet):
    """Total count a queryset."""
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse(data={'total': queryset.count()}, status=200)


class GroupCountModelMixin(GenericViewSet):
    """Count a queryset by group."""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    default_group_by_field = 'id'  # string, field
    default_time_unit = ''  # string, type(group_by_field)=DateTimeField --> year | month | day
    time_unit_str = {
        'year': '%%Y',
        'month': '%%Y-%%m',
        'week': '%%x-%%v',
        'day': '%%Y-%%m-%%d',
    }

    def list(self, request, *args, **kwargs):
        """
        分组查询
        :param request:
            group_by_field: 分组字段
            time_unit: 若按时间分组，可设置时间单位 year | month | day
        :param args:
        :param kwargs:
        :return:
        """
        group_by_field = self.default_group_by_field
        time_unit = self.default_time_unit
        if 'group_by_field' in request.query_params:
            request.query_params._mutable = True
            group_by_field = request.query_params.get('group_by_field')
            request.query_params.__delitem__('group_by_field')
            request.query_params._mutable = False

        if 'time_unit' in request.query_params:
            request.query_params._mutable = True
            time_unit = request.query_params.get('time_unit')
            request.query_params.__delitem__('time_unit')
            request.query_params._mutable = False

        extra_select = {
            group_by_field: "DATE_FORMAT({}, '{}')".format(group_by_field, self.time_unit_str[time_unit])
        } if time_unit else {}
        queryset = self.filter_queryset(self.get_queryset().extra(select=extra_select).values(group_by_field)).\
            order_by(group_by_field).annotate(count=Count("id")).values(group_by_field, "count")
        return JsonResponse(data=list(queryset.all()), status=200)


if __name__ == '__main__':
    pass
