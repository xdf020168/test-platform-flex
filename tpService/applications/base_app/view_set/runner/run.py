#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:run
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

import traceback

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from loguru import logger

from applications.system_mgr.models import SysSetting
from commons.drf_base import JsonResponse
from applications.base_app.view_set.runner.run_pytest import run_pytest_with_logger


class TestRunViewSet(CreateModelMixin, GenericViewSet):
    def create(self, request, *args, **kwargs):
        """执行测试 - post"""
        try:
            report_id, summary = run_pytest_with_logger(request.data)
            return JsonResponse(data=summary, msg='测试执行完成！(报告ID：{})'.format(report_id), success='true', status=200)
        except Exception as e:
            logger.error(traceback.format_exc())
            # raise e  # debug
            # traceback.format_exc(limit=3)
            debug = SysSetting.objects.first().data.get('debug')
            data = '{}\n\n{}'.format(e, traceback.format_exc()) if debug else str(e)
            return JsonResponse(data=data, msg=str(e).split('\n')[0], success='false', status=200)


if __name__ == '__main__':
    pass
