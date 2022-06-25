#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:argument
@time:2022/06/25
@email:tao.xu2008@outlook.com
@description: set web subparsers
"""


def set_web_runner_subparsers(action):
    """
    set subparsers for web_runner
    :param action:
    :return:
    """

    # api
    sub_parser = action.add_parser('web', help='sub command of WEB TEST')
    sub_parser.set_defaults(module='web')
    sub_parser.add_argument("--project", required=False, action="store", dest="project_name",
                            default="project_1", choices=['project_1', 'project_2'], help="测试项目选择")
    sub_parser.add_argument("--env", required=False, action="store", dest="env_name",
                            default="env_1", choices=['env_1', 'env_2'], help="测试环境选择")
    sub_parser.add_argument("--data", action="store", dest="data_subdir_list", nargs='+',
                            default=[], help="指定测试用例目录*/data/下子目录")
    sub_parser.add_argument("--exclude_data", action="store", dest="exclude_data_subdir_list", nargs='+',
                            default=[], help="排除测试用例目录*/data/下子目录")
    sub_parser.add_argument("--build_type", required=False, action="store", dest="build_type",
                            default="冒烟测试", choices=['冒烟测试', '其他'], help="测试构建类型选择")


if __name__ == "__main__":
    pass
