#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_report.py
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 测试报告
"""
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from config import global_cf
from libs.jenkins_opt import JenkinsOperation

from commons.drf_base import JsonResponse, BaseViewSet
from applications.base_app.models import TestReport
from applications.base_app.filters import TestReportFilter
from applications.base_app.serializers import TestReportSerializer, TestReportDeserializer


class TestReportViewSet(BaseViewSet):
    serializer_class = TestReportSerializer
    queryset = TestReport.objects.all().order_by('-id')
    filterset_class = TestReportFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().update(request, *args, **kwargs)

    # 局部更新数据
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = TestReportDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


class PytestHtmlViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        """获取报告HTML内容"""
        report_id = kwargs.get('pk')
        try:
            report = TestReport.objects.get(id__exact=report_id)
            with open(report.html_report_path, 'r', encoding='utf-8') as f:
                page = f.read()
            return JsonResponse(page.encode(encoding='utf-8'), status=200)
        except Exception as e:
            print(e)
            return JsonResponse(str(e), status=200)


class JenkinsAllureViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        """获取Jenkins报告地址"""
        report_id = kwargs.get('pk')
        try:
            report = TestReport.objects.get(id__exact=report_id)
            build_number = report.jenkins_build_number
            jenkins_conf = global_cf.get_kvs('JENKINS')
            job_name = jenkins_conf.get('job_name')
            jenkins_opt = JenkinsOperation(
                url=jenkins_conf.get('url'),
                user=jenkins_conf.get('user'),
                password=jenkins_conf.get('password'),
            )
            allure_url = report.allure_url
            if not allure_url and build_number and build_number > 0:
                allure_url = jenkins_opt.get_build_allure_url(job_name, build_number)
                report.allure_url = allure_url
                report.save()
            return JsonResponse(allure_url, status=200)
        except Exception as e:
            print(e)
            return JsonResponse(str(e), status=200)


class TestLogsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        """获取报告log内容"""
        report_id = kwargs.get('pk')
        try:
            report = TestReport.objects.get(id__exact=report_id)
            with open(report.log_path, 'r', encoding='utf-8') as f:
                page = f.read()
            return JsonResponse(page.encode(encoding='utf-8'), status=200)
        except Exception as e:
            print(e)
            return JsonResponse(str(e), status=200)


if __name__ == '__main__':
    pass
