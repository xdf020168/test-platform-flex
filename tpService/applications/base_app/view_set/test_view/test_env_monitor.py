#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_env_monitor
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 测试环境验证、状态监控
"""
import copy
from loguru import logger
from commons.drf_base import BaseViewSet
from applications.base_app.models import TestEnvMonitor, TestReport, GlobalEnv
from applications.base_app.filters import TestEnvMonitorFilter
from applications.base_app.serializers import TestEnvMonitorSerializer, TestEnvMonitorDeserializer
from applications.base_app.task_mgr.scheduler import Scheduler
from applications.base_app.view_set.runner.run_pytest import run_pytest_with_logger


def update_env_monitor_report_id(env_monitor):
    """
    查询最近一次报告并写入
    :param env_monitor:
    :return: 写入成功返回True，未写入返回False
    """
    # 查询最近一次报告并写入
    env = env_monitor['env']
    build_type = env_monitor['build_type']
    env_id = env if isinstance(env, (int, str)) else env['id']
    report = TestReport.objects.filter(env__id__exact=env_id, build_type__exact=build_type, is_delete__exact=False).order_by('-create_time').first()
    if report:
        TestEnvMonitor.objects.filter(id__exact=env_monitor['id']).update(report=report.id)
        return True
    return False


def remove_cron_job(job_id):
    try:
        logger.info('删除原有 cron_job: {}'.format(job_id))
        Scheduler().remove_job(job_id)
    except Exception as e:
        logger.error(e)


def add_cron_job(env_monitor: dict) -> None:
    job_id = env_monitor.get('id')
    # 删除原有 cron_job
    remove_cron_job(job_id)

    cron = env_monitor.get('cron')
    if cron:
        # 新建 cron_job
        try:
            env_id = env_monitor.get('env')
            validate_id = env_monitor.get('validate')
            env = GlobalEnv.objects.filter(id=env_id).first()
            task_name = "{}_{}_{}".format(env.id, env.name, env.description)
            kwargs = {
                'data': {
                    'env': env,
                    'validate': {'id': validate_id},
                    'build_type': env_monitor.get('build_type'),
                    'level': 'test_case',
                    'list': 'all',
                    'filters': {}
                }
            }
            logger.info('新建 cron_job: {}'.format(job_id))
            Scheduler().add_cron_job(
                job_id, task_name, cron,
                func=run_pytest_with_logger,
                kwargs=kwargs
            )
        except Exception as e:
            logger.error(e)
            logger.error('定时任务添加失败！')
    return


class TestEnvMonitorViewSet(BaseViewSet):
    serializer_class = TestEnvMonitorSerializer
    queryset = TestEnvMonitor.objects.all().order_by('env__name')
    filterset_class = TestEnvMonitorFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        Scheduler().get_cron_jobs_info(response.data['data']['list'])
        for d in copy.deepcopy(response.data['data']['list']):
            job_id = d.get('id')
            TestEnvMonitor.objects.filter(id__exact=job_id).update(cron_job=d['cron_job'])

        env_monitors = response.data.get('data').get('list')
        updated = False
        for env_monitor in env_monitors:
            up = update_env_monitor_report_id(env_monitor)
            if up:
                updated = True
        if updated:
            return super().list(request, *args, **kwargs)
        return response

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        response = super().update(request, *args, **kwargs)
        data = response.data.get('data')
        add_cron_job(data)
        update_env_monitor_report_id(data)
        return response

    # 局部更新数据
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        response = super().update(request, *args, **kwargs)
        data = response.data.get('data')
        add_cron_job(data)
        update_env_monitor_report_id(data)
        return response

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        response = super().create(request, *args, **kwargs)
        data = response.data.get('data')

        # 定时任务：测试任务添加到Scheduler，加入定时执行队列
        logger.info('添加测试任务到Scheduler，加入定时执行队列...')
        add_cron_job(data)

        # 测试环境暂无关联报告，查询最近一次报告并写入
        logger.info('新建环境监控暂无关联报告，查询最近一次报告并写入...')
        update_env_monitor_report_id(data)
        return response

    # 删除数据
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        job_id = int(kwargs['pk'])
        remove_cron_job(job_id)
        return response

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = TestEnvMonitorDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
