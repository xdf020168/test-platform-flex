#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_suite
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""
from commons.drf_base import BaseViewSet, GroupCountModelMixin, TotalCountModelMixin
from applications.base_app.models import TestSuite
from applications.base_app.serializers import TestSuiteSerializer, TestSuiteDeserializer
from applications.base_app.filters import TestSuiteFilter


class TestSuiteViewSet(BaseViewSet):
    serializer_class = TestSuiteSerializer
    queryset = TestSuite.objects.all().order_by('id')
    filterset_class = TestSuiteFilter

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().create(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().update(request, *args, **kwargs)

    # 局部更新数据
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().update(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = TestSuiteDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


# 统计数据
class TestSuiteTotalViewSet(TotalCountModelMixin):
    """获取接口总数数据"""
    filterset_class = TestSuiteFilter
    queryset = TestSuite.objects.filter(status__exact=True)


class TestSuiteCountViewSet(GroupCountModelMixin):
    """获取测试用例集统计数据"""
    filterset_class = TestSuiteFilter
    queryset = TestSuite.objects.filter(status__exact=True)
    default_group_by_field = 'department'
    default_time_unit = None


if __name__ == '__main__':
    pass
