#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:base_models
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 接口测试相关数据表模型
"""
from django.db import models

from applications.base_app.models import BaseModel


# 系统配置
def default_sys_setting():
    setting = {
        "debug": {"value": True, "description": "Debug模式"},
        "file_log_level": {"value": 'DEBUG', "description": "日志等级（文件）"},
        "console_log_level": {"value": 'INFO', "description": "日志等级（控制台）"},
        "history_max_rotation": {"value": 50, "description": "保留历史构建数据的最大个数"}
    }
    return setting


class SysSetting(BaseModel):
    """系统配置，如debug模式、历史构建保留数等"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, default='系统配置', verbose_name='Name')
    data = models.JSONField(default=default_sys_setting, verbose_name='系统配置数据')

    def delete(self, using=None, keep_parents=False):
        return "系统配置，禁止删除!"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_app_setting():
        return default_sys_setting()

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
