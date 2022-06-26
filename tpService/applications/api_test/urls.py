#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:urls
@time:2022/06/26
@email:tao.xu2008@outlook.com
@description:
"""
from django.urls import path, include, re_path
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from applications.api_test.view_set.test_view.test_report import TestReportViewSet, PytestHtmlViewSet, \
    JenkinsAllureViewSet, TestLogsViewSet

# router = DefaultRouter()
router = BulkRouter()

# 测试报告
router.register(r'test/report/bulk', TestReportViewSet),  # 批量处理
router.register(r'test/report/list', TestReportViewSet, basename='list'),
router.register(r'test/report/detail', TestReportViewSet, basename='retrieve'),
router.register(r'test/report/update', TestReportViewSet, basename='update'),
router.register(r'test/report/pytest_html', PytestHtmlViewSet, basename='retrieve'),
router.register(r'test/report/jenkins_allure', JenkinsAllureViewSet, basename='retrieve'),
router.register(r'test/report/logs', TestLogsViewSet, basename='retrieve'),

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 数据表管理
    path('', include(router.urls)),

]


if __name__ == '__main__':
    pass
