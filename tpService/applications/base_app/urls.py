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

from applications.base_app.view_set.org_view.department import DepartmentViewSet
from applications.base_app.view_set.org_view.project import ProjectViewSet
from applications.base_app.view_set.global_view.global_env import GlobalEnvViewSet, EnvDataViewSet, \
    GetEnvDefaultConfigView
from applications.base_app.view_set.global_view.global_const import GlobalConstViewSet
from applications.base_app.view_set.global_view.global_label import GlobalLabelViewSet
from applications.base_app.view_set.test_view.test_suite import TestSuiteViewSet, TestSuiteCountViewSet, TestSuiteTotalViewSet
from applications.base_app.view_set.test_view.test_case import TestCaseViewSet, TestCaseCountViewSet, TestCaseTotalViewSet
from applications.base_app.view_set.test_view.test_step import TestStepViewSet, TestStepCountViewSet, TestStepTotalViewSet
from applications.base_app.view_set.test_view.test_report import TestReportViewSet, PytestHtmlViewSet, \
    JenkinsAllureViewSet, TestLogsViewSet
from applications.base_app.view_set.test_view.test_env_monitor import TestEnvMonitorViewSet
from applications.base_app.view_set.test_view.test_task import TestTaskViewSet

from applications.base_app.view_set.help_view.comparators import ComparatorHelpViewSet
from applications.base_app.view_set.help_view.functions import BuiltinFunctionHelpViewSet
from applications.base_app.view_set.runner.run import TestRunViewSet


# router = DefaultRouter()
router = BulkRouter()

# department
router.register(r'department/bulk', DepartmentViewSet),  # 批量处理
router.register(r'department/list', DepartmentViewSet, basename='list'),
router.register(r'department/detail', DepartmentViewSet, basename='retrieve'),
router.register(r'department/add', DepartmentViewSet, basename='create'),
router.register(r'department/update', DepartmentViewSet, basename='update'),
router.register(r'department/del', DepartmentViewSet, basename='destroy')

# project
router.register(r'project/bulk', ProjectViewSet),  # 批量处理
router.register(r'project/list', ProjectViewSet, basename='list'),
router.register(r'project/detail', ProjectViewSet, basename='retrieve'),
router.register(r'project/add', ProjectViewSet, basename='create'),
router.register(r'project/update', ProjectViewSet, basename='update'),
router.register(r'project/del', ProjectViewSet, basename='destroy')

# global env 环境配置
router.register(r'global/env/bulk', GlobalEnvViewSet),
router.register(r'global/env/list', GlobalEnvViewSet, basename='list'),
router.register(r'global/env/detail', GlobalEnvViewSet, basename='retrieve'),
router.register(r'global/env/add', GlobalEnvViewSet, basename='create'),
router.register(r'global/env/update', GlobalEnvViewSet, basename='update'),
router.register(r'global/env/del', GlobalEnvViewSet, basename='destroy'),
router.register(r'global/env/data', EnvDataViewSet, basename='retrieve'),


# global const
router.register(r'global/const/bulk', GlobalConstViewSet),
router.register(r'global/const/list', GlobalConstViewSet, basename='list'),
router.register(r'global/const/detail', GlobalConstViewSet, basename='retrieve'),
router.register(r'global/const/add', GlobalConstViewSet, basename='create'),
router.register(r'global/const/update', GlobalConstViewSet, basename='update'),
router.register(r'global/const/del', GlobalConstViewSet, basename='destroy'),

# global label
router.register(r'global/label/bulk', GlobalLabelViewSet),
router.register(r'global/label/list', GlobalLabelViewSet, basename='list'),
router.register(r'global/label/detail', GlobalLabelViewSet, basename='retrieve'),
router.register(r'global/label/add', GlobalLabelViewSet, basename='create'),
router.register(r'global/label/update', GlobalLabelViewSet, basename='update'),
router.register(r'global/label/del', GlobalLabelViewSet, basename='destroy'),

# test suite
router.register(r'test/suite/bulk', TestSuiteViewSet),  # 批量处理
router.register(r'test/suite/list', TestSuiteViewSet, basename='list'),
router.register(r'test/suite/detail', TestSuiteViewSet, basename='detail'),
router.register(r'test/suite/add', TestSuiteViewSet, basename='create'),
router.register(r'test/suite/update', TestSuiteViewSet, basename='update'),
router.register(r'test/suite/del', TestSuiteViewSet, basename='destroy'),
router.register(r'test/suite/total', TestSuiteTotalViewSet, basename='list'),
router.register(r'test/suite/count', TestSuiteCountViewSet, basename='list'),

# test case
router.register(r'test/case/bulk', TestCaseViewSet),  # 批量处理
router.register(r'test/case/list', TestCaseViewSet, basename='list'),
router.register(r'test/case/detail', TestCaseViewSet, basename='retrieve'),
router.register(r'test/case/add', TestCaseViewSet, basename='create'),
router.register(r'test/case/update', TestCaseViewSet, basename='update'),
router.register(r'test/case/del', TestCaseViewSet, basename='destroy'),
router.register(r'test/case/total', TestCaseTotalViewSet, basename='list'),
router.register(r'test/case/count', TestCaseCountViewSet, basename='list'),

# test step
router.register(r'test/step/bulk', TestStepViewSet),  # 批量处理
router.register(r'test/step/list', TestStepViewSet, basename='list'),
router.register(r'test/step/detail', TestStepViewSet, basename='retrieve'),
router.register(r'test/step/add', TestStepViewSet, basename='create'),
router.register(r'test/step/update', TestStepViewSet, basename='update'),
router.register(r'test/step/del', TestStepViewSet, basename='destroy'),
router.register(r'test/step/total', TestStepTotalViewSet, basename='list'),
router.register(r'test/step/count', TestStepCountViewSet, basename='list'),

# 测试执行
router.register(r'test/run', TestRunViewSet, basename='create'),


# 测试环境验证、状态监控
router.register(r'test/env_monitor/bulk', TestEnvMonitorViewSet),  # 批量处理
router.register(r'test/env_monitor/list', TestEnvMonitorViewSet, basename='list'),
router.register(r'test/env_monitor/detail', TestEnvMonitorViewSet, basename='retrieve'),
router.register(r'test/env_monitor/add', TestEnvMonitorViewSet, basename='create'),
router.register(r'test/env_monitor/update', TestEnvMonitorViewSet, basename='update'),
router.register(r'test/env_monitor/del', TestEnvMonitorViewSet, basename='destroy'),

# 测试任务
# router.register(r'test/task/bulk', TestTaskViewSet),  # 批量处理 - 暂不支持
router.register(r'test/task/add', TestTaskViewSet, basename='create'),
router.register(r'test/task/update', TestTaskViewSet, basename='update'),
router.register(r'test/task/del', TestTaskViewSet, basename='destroy'),
router.register(r'test/task/list', TestTaskViewSet, basename='list'),
router.register(r'test/task/detail', TestTaskViewSet, basename='retrieve'),

# 帮助信息
router.register(r'help/comparator/list', ComparatorHelpViewSet, basename='list'),
router.register(r'help/builtin_functions/list', BuiltinFunctionHelpViewSet, basename='list')

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

    # 获取env默认数据
    re_path(r'global/env/config/default', GetEnvDefaultConfigView.as_view()),

]


if __name__ == '__main__':
    pass
