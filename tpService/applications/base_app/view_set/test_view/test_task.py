#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_task
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

import copy
from commons.drf_base import BaseViewSet
from applications.base_app.models import TestTask
from applications.base_app.serializers import TestTaskSerializer, TestTaskDeserializer
from applications.base_app.filters import TestTaskFilter
from applications.base_app.task_mgr.scheduler import Scheduler
from applications.base_app.view_set.runner.run_pytest import run_with_filters


class TestTaskViewSet(BaseViewSet):
    serializer_class = TestTaskSerializer
    queryset = TestTask.objects.all().order_by('-id')
    filterset_class = TestTaskFilter

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestTaskDeserializer
        # 插入 api_test_testtask 表
        response = super().create(request, *args, **kwargs)

        # 定时任务：测试任务添加到Scheduler，加入定时执行队列
        task = response.data.get('data')
        task_cron = task.get('cron')
        if task_cron:
            task_id = task.get('id')
            task_name = task.get('name')
            task_env = task.get('task_env')
            task_validate = task.get('task_validate')
            task_level = task.get('task_level')
            task_filters = task.get('task_filters', {})
            Scheduler().add_cron_job(
                task_id, task_name, task_cron,
                func=run_with_filters,
                args=(task_env, task_validate, task_level, task_filters)
            )

        return response

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestTaskDeserializer
        response = super().update(request, *args, **kwargs)
        task = response.data.get('data')
        task_id = task.get('id')
        task_name = task.get('name')
        task_cron = task.get('cron')
        if task_cron:
            Scheduler().edit_cron_job(task_id, task_name, task_cron)
        return response

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # 查询数据
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        Scheduler().list_job(response.data['data']['list'])
        for t in copy.deepcopy(response.data['data']['list']):
            if t.get('status') < 2:
                task_id = t.get('id')
                t.pop('test_env')
                t.pop('test_validate')
                TestTask.objects.filter(id__exact=task_id).update(**t)
        return response

    # 删除数据
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        task_id = int(kwargs['pk'])
        Scheduler().remove_job(task_id)
        return response


if __name__ == '__main__':
    pass
