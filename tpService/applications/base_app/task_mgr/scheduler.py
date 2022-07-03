#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:scheduler
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: Advanced Python Scheduler，在指定的时间规则执行指定的作业
"""

import json
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception as e:
            return str(obj)


class Scheduler(object):
    scheduler: AsyncIOScheduler = None

    @staticmethod
    def init(scheduler):
        Scheduler.scheduler = scheduler

    @staticmethod
    def configure(**kwargs):
        Scheduler.scheduler.configure(**kwargs)

    @staticmethod
    def start():
        Scheduler.scheduler.start()

    # 新增 - 定时调度任务
    @staticmethod
    def add_cron_job(job_id, task_name, cron, func, args=None, kwargs=None):
        return Scheduler.scheduler.add_job(func=func, args=args, kwargs=kwargs,
                                           name=task_name, id=str(job_id),
                                           trigger=CronTrigger.from_crontab(cron))

    @staticmethod
    def edit_cron_job(job_id, task_name, cron):
        """
        通过task id，更新任务的cron，name等数据
        :param job_id:
        :param task_name:
        :param cron:
        :return:
        """
        Scheduler.scheduler.modify_job(job_id=str(job_id), trigger=CronTrigger.from_crontab(cron), name=task_name)
        Scheduler.scheduler.pause_job(str(job_id))
        Scheduler.scheduler.resume_job(str(job_id))

    @staticmethod
    def pause_resume_job(job_id, status):
        """
        暂停或恢复task，会影响到next_run_at
        :param job_id:
        :param status:
        :return:
        """
        if status:
            Scheduler.scheduler.resume_job(job_id=str(job_id))
        else:
            Scheduler.scheduler.pause_job(job_id=str(job_id))

    @staticmethod
    def remove_job(job_id):
        """
        删除job，当删除测试计划时，调用此方法
        :param job_id:
        :return:
        """
        Scheduler.scheduler.remove_job(str(job_id))

    @staticmethod
    def list_job(data: List):
        for d in data:
            job = Scheduler.scheduler.get_job(str(d.get('id')))
            if job is None:
                if d['cron']:
                    # 说明job初始化失败了
                    d["status"] = 5  # '异常'
                else:
                    # 说明job初始化失败了 --  cron 空，无效
                    d["status"] = 4  # '无效'
                continue
            d['job_state'] = json.loads(json.dumps(job.__getstate__(), cls=MyEncoder, ensure_ascii=False))
            if job.next_run_time is None:
                # 说明job被暂停了
                d["status"] = 3  # '暂停'
            else:
                d["next_run"] = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_cron_jobs_info(data: List):
        for d in data:
            job_id = d.get('id')
            job_info = {'id': job_id}
            job = Scheduler.scheduler.get_job(str(job_id))
            if job is None:
                continue
            job_info['job_state'] = json.loads(json.dumps(job.__getstate__(), cls=MyEncoder, ensure_ascii=False))
            if job.next_run_time is None:
                job_info["next_run_time"] = ''
            else:
                job_info["next_run_time"] = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
            d['cron_job'] = job_info


if __name__ == '__main__':
    pass
