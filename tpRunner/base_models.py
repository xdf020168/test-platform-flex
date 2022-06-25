#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:models
@time:2022/04/03
@email:tao.xu2008@outlook.com
@description:公共数据模型定义
"""
from enum import Enum
from typing import Dict, List, Text, Union

from pydantic import BaseModel


# 测试平台信息
class PlatformInfo(BaseModel):
    runner_name: Text
    runner_version: Text
    python_version: Text
    platform: Text


# 测试步骤类型
class StepType(Text, Enum):
    """测试步骤类型枚举"""
    UNKNOWN = ''  # 未知、未定义
    API = 'API'  # rest_api 测试
    WEB = 'WEB'  # Web UI 测试
    SDK = 'SDK'  # SDK 调用
    CMD = 'CMD'  # OS CMD 命令执行
    UC = 'UC'  # UC 命令执行
    CASE_REF = 'CASE_REF'  # 步骤为测试用例引用


# 测试结果 - 状态枚举
class TestStatusEnum(Text, Enum):
    """测试结果状态枚举"""
    UNKNOWN = ''
    PASSED = 'passed'
    FAILED = 'failed'
    ERROR = 'error'
    SKIPPED = 'skipped'
    BROKEN = 'broken'


# 测试结果 - 统计
class TestStat(BaseModel):
    """测试结果统计"""
    total: int = 0
    passed: int = 0
    failed: int = 0
    error: int = 0
    skipped: int = 0
    # 记录失败、故障、跳过的用例/步骤详情
    failed_list: List[Dict] = []  # [{},{}]
    error_list: List[Dict] = []  # [{},{}]
    skipped_list: List[Dict] = []  # [{},{}]


# 测试执行时间
class TestTime(BaseModel):
    """测试用例执行时间"""
    start_at: float = 0
    end_at: float = 0
    duration: float = 0
    start_at_format: Text = ""
    end_at_format: Text = ""
    duration_format: Text = ""


# 测试报告 - 结果概览
class ReportSummary(BaseModel):
    """测试报告概要收集"""
    success: bool = True
    id: Text = ""
    name: Text = "xxx测试报告"
    description: Text = "xxx测试报告"
    status: TestStatusEnum = TestStatusEnum.UNKNOWN
    time: TestTime = TestTime()
    testcases_stat: TestStat = TestStat()
    teststeps_stat: TestStat = TestStat()
    log: Text = ''
    allure_xml_path: Text = ''
    html_report_path: Text = ''


class DBInfo(BaseModel):
    """数据库连接信息"""
    ENGINE: Text = "django.db.backends.sqlite3",  # django.db.backends.mysql
    NAME: Text = "",  # sqlite3: sqlite3.db path, mysql:database_name
    USER: Text = "",
    PASSWORD: Text = "",
    HOST: Text = "",
    PORT: int = 0,


if __name__ == '__main__':
    pass
