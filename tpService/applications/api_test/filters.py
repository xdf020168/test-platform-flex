#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:filters.py
@time:2022/06/26
@email:tao.xu2008@outlook.com
@description: 过滤器
"""

import django_filters
from django_filters.rest_framework import FilterSet
from django.utils.translation import gettext_lazy as _

from applications.api_test.models import Project, GlobalEnv, TestReport


class BaseAnyInFilter(django_filters.Filter):
    """TODO"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'any_in')
        kwargs.setdefault('help_text', _('Multiple values may be separated by commas.'))
        super().__init__(*args, **kwargs)

        class ConcreteCSVField(self.base_field_class, self.field_class):
            pass

        ConcreteCSVField.__name__ = self._field_class_name(
            self.field_class, self.lookup_expr
        )

        self.field_class = ConcreteCSVField


class NumberAnyInFilter(BaseAnyInFilter, django_filters.NumberFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ProjectFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    department__isnull = django_filters.CharFilter(field_name='department__id', lookup_expr='isnull')

    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            # 'department': ['exact']
        }


class GlobalEnvFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = GlobalEnv
        fields = {
            'name': ['exact']
        }


class TestReportFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    create_time__gte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    create_time__lte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = TestReport
        fields = {
            'id': ['exact'],
            'status': ['exact'],
            'env': ['exact'],
            'build_type': ['exact']
        }


if __name__ == '__main__':
    pass
