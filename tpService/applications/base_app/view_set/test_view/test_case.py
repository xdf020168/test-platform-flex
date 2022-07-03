#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_case
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

from commons.drf_base import BaseViewSet, GroupCountModelMixin, TotalCountModelMixin
from applications.base_app.models import TestCase
from applications.base_app.filters import TestCaseFilter
from applications.base_app.serializers import TestCaseSerializer, TestCaseDeserializer


class TestCaseViewSet(BaseViewSet):
    serializer_class = TestCaseSerializer
    queryset = TestCase.objects.all().order_by('id')
    filterset_class = TestCaseFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().update(request, *args, **kwargs)

    # 局部更新数据
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = TestCaseDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


# 统计数据
class TestCaseTotalViewSet(TotalCountModelMixin):
    """获取接口总数数据"""
    filterset_class = TestCaseFilter
    queryset = TestCase.objects.filter(status__exact=True)


class TestCaseCountViewSet(GroupCountModelMixin):
    """获取测试用例统计数据"""
    filterset_class = TestCaseFilter
    queryset = TestCase.objects.filter(status__exact=True)
    default_group_by_field = 'type'
    default_time_unit = None


if __name__ == '__main__':
    pass
