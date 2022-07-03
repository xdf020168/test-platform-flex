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

from applications.base_app.models import Project, GlobalConst, GlobalEnv, GlobalLabel, TestSuite, TestCase, TestStep, \
    TestReport, TestTask, TestEnvMonitor


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


class GlobalConstFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = GlobalConst
        fields = {
            'name': ['exact']
        }


class GlobalEnvFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = GlobalEnv
        fields = {
            'name': ['exact']
        }


class GlobalLabelFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = GlobalLabel
        fields = {
            'name': ['exact'],
            'type': ['exact']
        }


class TestSuiteFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    department__in = NumberInFilter(field_name='department__id', lookup_expr='in')
    department__isnull = django_filters.CharFilter(field_name='department__id', lookup_expr='isnull')
    labels__in = django_filters.BaseInFilter(field_name='labels', lookup_expr='in')

    class Meta:
        model = TestSuite
        fields = {
            'id': ['exact'],
            'name': ['icontains'],
            'department': ['exact']
        }


class TestCaseFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type__in = django_filters.BaseInFilter(field_name='type', lookup_expr='in')
    result__in = django_filters.BaseInFilter(field_name='result', lookup_expr='in')
    test_suite__in = NumberInFilter(field_name='test_suite', lookup_expr='in')
    department__in = NumberInFilter(field_name='test_suite__department__id', lookup_expr='in')
    label__contains = django_filters.NumberFilter(field_name='labels__id', lookup_expr='contains')
    labels__name__contains = django_filters.CharFilter(field_name='labels__name', lookup_expr='contains')
    create_time__gte = django_filters.DateFilter(field_name='create_time', lookup_expr='gte')
    create_time__lte = django_filters.DateFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = TestCase
        fields = {
            'id': ['exact'],
            'name': ['icontains'],
            'test_suite': ['exact']
        }


class TestStepFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    result__in = django_filters.BaseInFilter(field_name='result', lookup_expr='in')
    test_case__in = NumberInFilter(field_name='test_case', lookup_expr='in')
    apiInfo__in = NumberInFilter(field_name='apiInfo', lookup_expr='in')
    apiInfo__project__in = NumberInFilter(field_name='apiInfo__project', lookup_expr='in')
    department__in = NumberInFilter(field_name='test_case__test_suite__department', lookup_expr='in')
    create_time__gte = django_filters.DateFilter(field_name='create_time', lookup_expr='gte')
    create_time__lte = django_filters.DateFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = TestStep
        fields = {
            'id': ['exact'],
            'name': ['exact'],
            'description': ['icontains'],
            'test_case': ['exact']
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


class TestTaskFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    create_time__gte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    create_time__lte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = TestTask
        fields = {
            'id': ['exact'],
            'status': ['exact'],
        }


class TestEnvMonitorFilter(FilterSet):
    id_in = NumberInFilter(field_name='id', lookup_expr='in')
    build_type = django_filters.CharFilter(field_name='build_type', lookup_expr='exact')
    env_name_icontains = django_filters.CharFilter(field_name='env__name', lookup_expr='icontains')
    create_time__gte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    create_time__lte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = TestEnvMonitor
        fields = {
            'id': ['exact'],
            'status': ['exact'],
            'build_type': ['exact'],
        }


if __name__ == '__main__':
    pass
