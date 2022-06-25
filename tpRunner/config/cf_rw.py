#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:cf_rw
@time:2022/04/03
@email:tao.xu2008@outlook.com
@description:
"""

import os
import codecs
import configparser

import yaml
from loguru import logger

from utils.exceptions import EnvNotFound, VariableNotFound


# 设置全局 key/value
_global_dict = {}


def set_global_value(key, value):
    """
    设置全局变量
    :param key:
    :param value:
    :return:
    """
    global _global_dict
    # print(key, value)
    _global_dict[key] = value


def get_global_value(key):
    """
    获取全局变量中key对应的值
    :param key:
    :return:
    :exception: 如果没找到，raise VariableNotFound
    """
    try:
        global _global_dict
        return _global_dict[key]
    except KeyError:
        raise VariableNotFound(key)


def get_global_dict():
    """获取整个全局变量字典"""
    return _global_dict


# 设置环境变量
def set_os_environ(variables_mapping):
    """
    设置系统环境变量的key/value：os.environ
    :param variables_mapping:
    :return:
    """
    for variable in variables_mapping:
        os.environ[variable] = variables_mapping[variable]
        logger.debug(f"Set OS environment variable: {variable}")


def unset_os_environ(variables_mapping):
    """
    删除系统环境变量中的key/value：os.environ
    :param variables_mapping:
    :return:
    """
    for variable in variables_mapping:
        os.environ.pop(variable)
        logger.debug(f"Unset OS environment variable: {variable}")


def get_os_environment(variable_name):
    """
    获取系统环境变量值
    :param variable_name:
    :return:
    :exception: 如果没找到，raise EnvNotFound
    """
    try:
        return os.environ[variable_name]
    except KeyError:
        raise EnvNotFound(variable_name)


# 读取配置文件
def read_yaml(file_path, yaml_loader=yaml.FullLoader):
    """
    读取yaml文件内容，返回字典
    :param file_path:
    :param yaml_loader:
    :return:
    """
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = yaml.load(f, Loader=yaml_loader)
    return data


def read_ini(file_path, section, option):
    """
    读取ini配置文件section->option的值，如：
    [TEST]
    url = https://xxxxx.com
    :param file_path:
    :param section: --TEST
    :param option: --url
    :return:
    """
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return conf.get(section, option)


def read_ini_section(file_path, section):
    """
    读取ini配置文件section下所有键值对，返回字典
    :param file_path:
    :param section:
    :return:
    """
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return dict(conf.items(section))


class ConfigIni(object):
    """读、写ini配置文件"""
    def __init__(self, file_path):
        """
        生成配置文件对象并读取配置文件
        :param file_path: 配置文件的绝对路径
        """
        self.file_path = file_path
        # 定义配置文件对象，并读取配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path, encoding='utf-8')

    # 获取字符串的配置内容
    def get_str(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value: 返回value的值
        """
        return self.cf.get(section, option)

    # 获取int数字型内容
    def get_int(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getint(section, option)

    # 获取float型数字内容
    def get_float(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getfloat(section, option)

    # 获取布尔值的返回内容
    def get_boolean(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getboolean(section, option)

    def get_kvs(self, section):
        return dict(self.cf.items(section))

    # 修改配置文件的value值
    def set_value(self, section, option, value):
        """
        修改value的值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :param value: 修改value的值
        :return:
        """
        # python内存先修改值
        self.cf.set(section, option, value)
        # 需要通过文件的方式写入才行，不然实体文件的值不会改变
        with open(self.file_path, "w+") as f:
            self.cf.write(f)
        return True


if __name__ == '__main__':
    pass
