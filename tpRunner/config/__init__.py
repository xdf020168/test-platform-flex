#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py
@time:2022/04/03
@email:tao.xu2008@outlook.com
@description: 全局配置，及配置文件读写方法。
"""
from datetime import datetime
from loguru import logger

from utils.util import zfill, to_safe_name, to_class_name
from config.cf_rw import *

logger.info("import config module...")

# 时间字符串
TIME_STR = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")  # 时间字符串
logger.info(TIME_STR)

# 项目root目录
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# 日志、报告目录路径
logs_dir = os.path.join(root_dir, "logs")
report_dir = os.path.join(root_dir, 'report')

# 测试用例设计文档目录路径
data_dir = os.path.join(root_dir, "tpRunner/api_runner/data")

# testcase目录路径
testcase_dir = os.path.join(root_dir, "tpRunner/api_runner/testcase")

# globals.ini 配置项
# 创建配置对象为全局变量
global_cf = ConfigIni(os.path.join(root_dir, 'tpRunner/config', 'globals.ini'))
FILE_LOG_LEVEL = global_cf.get_str("LOGGER", "file_level")
CONSOLE_LOG_LEVEL = global_cf.get_str("LOGGER", "console_level")
MAX_ROTATION = int(global_cf.get_str("LOGGER", "max_rotation"))


class TestSession(object):
    """生成基于report.id的测试session"""
    def __init__(self, project_name, env_name, report_id):
        self.project_name = to_class_name(project_name)
        self.env_name = to_safe_name(env_name)
        self.report_id = report_id
        self.zfill_report_id = zfill(report_id)
        self.log_level = FILE_LOG_LEVEL
        self.max_rotation = MAX_ROTATION

    @property
    def testcase_path(self):
        return os.path.join(testcase_dir, self.project_name, 'test_{}'.format(self.zfill_report_id))

    @property
    def log_path(self):
        return os.path.join(
            logs_dir,
            self.project_name,
            '{}-{}-{}-message.log'.format(self.zfill_report_id, self.env_name, TIME_STR)
        )

    @property
    def html_report_path(self):
        return os.path.join(report_dir, self.project_name, self.zfill_report_id, "html", "report.html")

    @property
    def xml_report_path(self):
        return os.path.join(report_dir, self.project_name, self.zfill_report_id, "xml")


__all__ = [
    "read_yaml", "ConfigIni",
    # 路径
    "root_dir", "logs_dir", "report_dir", "data_dir", "testcase_dir",
    # 全局内存变量读写
    "global_cf",
    "set_global_value", "get_global_value", "get_global_dict",
    # 环境变量读写
    "set_os_environ", "unset_os_environ", "get_os_environment",
    # 全局常量读取
    "TIME_STR",
    "FILE_LOG_LEVEL", "CONSOLE_LOG_LEVEL", "MAX_ROTATION",
    "TestSession"
]


if __name__ == '__main__':
    pass
