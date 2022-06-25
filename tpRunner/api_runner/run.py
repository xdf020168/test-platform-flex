#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:main
@time:2022/04/03
@email:tao.xu2008@outlook.com
@description: api_runner执行入口
"""
import os
import json
import argparse
import atexit

from loguru import logger
import subprocess

from tpRunner.utils import util
from tpRunner import config
from tpRunner.base_models import DBInfo
from tpRunner.utils.util import rm_tree, seconds_to_hms
from tpRunner.api_runner.core.maker import main_make
from tpRunner.api_runner.core.data_loader import load_testcase

from django.conf import settings
from tpService.applications.api_test.models import TestReport  # tpService.


def args_parser():
    """test args parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=False, action="store", dest="project_name",
                        default="project_1", choices=['project_1', 'project_2'], help="测试项目选择")
    parser.add_argument("--env", required=False, action="store", dest="env_name",
                        default="env_1", choices=['env_1', 'env_2'], help="测试环境选择")
    parser.add_argument("--data", action="store", dest="data_subdir_list", nargs='+',
                        default=[], help="指定测试用例目录*/data/下子目录")
    parser.add_argument("--exclude_data", action="store", dest="exclude_data_subdir_list", nargs='+',
                        default=[], help="排除测试用例目录*/data/下子目录")
    parser.add_argument("--build_type", required=False, action="store", dest="build_type",
                        default="冒烟测试", choices=['冒烟测试', '其他'], help="测试构建类型选择")

    pytest_group = parser.add_argument_group("pytest框架参数")
    pytest_group.add_argument("-k", action="store", dest="match_expr",
                              default="test_", help="执行匹配表达式的用例")

    jenkins_group = parser.add_argument_group("jenkins相关参数")
    jenkins_group.add_argument("--job_name", action="store", dest="job_name",
                               default="", help="Jenkins JOB_NAME")

    return parser


def _rm_rotation_files(args):
    tc_max_rotation = config.MAX_ROTATION
    project_name = args.project_name

    testcase_path = os.path.join(config.testcase_dir, project_name)
    log_path = os.path.join(config.logs_dir, project_name)
    report_path = os.path.join(config.report_dir, project_name)

    # - 删除旧的测试构建文件
    # testcase/test_*
    rm_tree(testcase_path, "test_*", max_rotation=tc_max_rotation)
    # reports/*
    rm_tree(log_path, "*", max_rotation=tc_max_rotation)
    # logs/runner/*
    rm_tree(report_path, "*", max_rotation=tc_max_rotation)


def _init_test_session(args):
    """
    初始化测试session数据，写入DB
    :param args:
    :return:
    """
    logger.info("初始化测试session数据...")
    # 参数解析
    project_name = args.project_name
    env_name = args.env_name
    config.set_global_value("env_name", env_name)
    config.set_global_value("project_name", project_name)

    logger.info("插入api_test_report数据表...")

    report = TestReport.objects.create(
        **{
            "create_time": config.TIME_STR,
            "build_type": args.build_type,
            "env_id": 1
        }
    )
    report_id = report.id

    # 定制测试session属性
    session_attr = config.TestSession(project_name, env_name, report_id)

    report.log_path = session_attr.log_path
    report.save()

    return session_attr


def _load_testcase_data(args):
    logger.info('加载用例文件'.center(70, '>'))
    try:
        data_subdir_list = args.data_subdir_list or [None]
        data_list = load_testcase(config.data_dir, data_subdir_list)
    except Exception as e:
        raise e
    return data_list


def _run_with_data(test_session, tc_data_list):
    """
    执行pytest
    :param test_session:
    :return:
    """
    # - 生成测试py文件
    logger.info("生成测试pytest文件...")
    pytest_files_run_set = main_make(tc_data_list, test_session.testcase_path)
    len_pytest_files = len(pytest_files_run_set)
    logger.info("待执行pytest用例文件({})：\n".format(len_pytest_files, util.json_dumps(pytest_files_run_set)))
    if len_pytest_files == 0:
        logger.error("无测试用例将被执行！")
        return 0, {}

    # - 获取数据库信息，并传入pytest
    default_db = settings.DATABASES.get('default')
    db_info = {
        "ENGINE": default_db.get('ENGINE'),
        "DB_PATH": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
        "NAME": "",
    }
    if default_db.get('ENGINE') == 'django.db.backends.sqlite3':
        db_info["DB_PATH"] = str(default_db.get('NAME'))
    elif default_db.get('ENGINE') == 'django.db.backends.mysql':
        db_info["USER"] = default_db.get('USER')
        db_info["PASSWORD"] = default_db.get('PASSWORD')
        db_info["HOST"] = default_db.get('HOST')
        db_info["PORT"] = default_db.get('PORT')
        db_info["NAME"] = default_db.get('NAME')
    # - 构建pytest 参数
    logger.info("构建pytest 参数...")
    argv = pytest_files_run_set + [
        '--log_path={}'.format(test_session.html_report_path),
        '--log_level={}'.format(test_session.log_level),
        '--db_info={}'.format(utils.json_dumps(db_info)),
        '--project_name={}'.format(test_session.project_name),
        '--env_name={}'.format(test_session.env_name),
        '--report_id={}'.format(test_session.report_id),
        '-v', '-s', '--ignore-unknown-dependency',
        '-W', 'ignore:Module already imported:pytest.PytestWarning',
        '--html={}'.format(test_session.html_report_path),
        '--self-contained-html',
        # '--capture=sys',
        '--allure-no-capture',  # 取消添加程序中捕获到控制台或者终端的log日志或者print输出到allure测试报告的Test Body中
        '--alluredir={}'.format(test_session.xml_report_path), '--clean-alluredir',  # 生成allure xml结果
    ]
    # -q test_01.py
    logger.info("pytest 命令：\n".format(json.dumps(argv, indent=2)))

    # - 执行pytest

    # 执行方式一
    # import pytest
    # pytest.main(argv)
    # err_msg = ''
    # exit_code = 0

    # 执行方式二
    p = subprocess.Popen(['pytest'] + argv)
    p.wait()

    # - 获取结果并返回
    reports = TestReport.objects.filter(id=test_session.report_id)
    if reports.count() == 0:
        raise Exception("未找到测试报告：{}".format(test_session.report_id))

    report = reports.first()
    report_id = report.id

    summary = {
        "status": report.status,
        "total": report.step_total,
        "pass": report.step_passed,
        "failed": report.step_failed,
        "error": report.step_error,
        "skipped": report.step_skipped,
        "pass_rate": "{}%".format(report.step_pass_rate * 100),
        "duration": seconds_to_hms(report.duration)
    }
    return report_id, summary


def _generate_allure_report(test_session):
    """
    从测试报告表中读取测试结果数据，生成allure报告。
    服务器运行：通过Jenkins生成allure报告
    本地运行：allure serve命令立即生成allure报告
    :param test_session:
    :return:
    """
    try:
        logger.info("generate allure report...")
        xml_report_path = test_session.xml_report_path
        if util.get_net_mac_address() == '00:16:3e:17:7c:40':
            # 47.99.145.123 服务器运行
            if not test_session.report_id:
                logger.error("无测试结果记录，跳过报告生成！")
                return

            from tpRunner.commons.jenkins_opt import JenkinsOperation
            # 创建配置对象为全局变量
            jenkins_conf = config.global_cf.get_kvs('JENKINS')
            job_name = jenkins_conf.get('job_name')
            token = jenkins_conf.get('token')
            jenkins_opt = JenkinsOperation(
                url=jenkins_conf.get('url'),
                user=jenkins_conf.get('user'),
                password=jenkins_conf.get('password'),
            )
            parameters = {
                'xml_report_path': xml_report_path
            }
            logger.info(xml_report_path)
            # 获取jenkins下一次build number并立即构建
            build_number = jenkins_opt.get_next_build_number(job_name)
            number = jenkins_opt.trigger_build_job(job_name, parameters, token)
            logger.info(number)
            # allure_url = jenkins_opt.get_build_allure_url(job_name, build_number)
            # 保存jenkins job/build信息到测试报告表，便于后期读取
            TestReport.objects.filter(id__exact=test_session.report_id).update(
                client='47.99.145.123',
                jenkins_job_name='test-platform-report',
                jenkins_build_number=build_number,
                # allure_url=allure_url
            )
        else:
            # 本地调试
            allure_serve_cmd = 'D:\\allure-2.16.1\\bin\\allure serve {}'.format(xml_report_path)
            logger.info(allure_serve_cmd)
            subprocess.Popen(allure_serve_cmd, shell=True, close_fds=True)
            # p.wait()
    except Exception as e:
        logger.error(e)


def run_pytest_with_logger(args):
    """
    pytest + logger
    :param args:
    :return:
    """
    # 初始化测试执行session - 供后续数据跟踪
    try:
        test_session = _init_test_session(args)
    except Exception as e:
        raise e

    handler_id = None
    try:
        # - 添加logger并执行测试。
        # 注：此处logger仅作用于pytest执行前的数据加载，pytest执行为新进程，需传相同log_path并在新进程中创建logger
        handler_id = logger.add(
            test_session.log_path,
            rotation='100 MB',
            retention='7 days',
            enqueue=True,
            encoding="utf-8",
            level=test_session.log_level
        )
        atexit.register(logger.remove)

        # - 删除旧的测试构建文件
        _rm_rotation_files(args)

        # - 加载、解析用例数据
        tc_data_list = _load_testcase_data(args)

        # - 执行 pytest
        return _run_with_data(test_session, tc_data_list)
    except Exception as e:
        raise e
    finally:
        logger.info("test log: {}".format(test_session.log_path))
        logger.info("result data: {}".format(test_session.xml_report_path))
        try:
            logger.remove(handler_id)
        except Exception as e:
            logger.error(e)
        reports = TestReport.objects.filter(id=test_session.report_id)
        if reports.count() > 0:
            report = reports.first()
            # 0执行，标记为 - 失败; 否则，生成报告
            if report.step_total == 0:
                # 无测试步骤被执行，标记为 - 失败
                report.status = False
                report.build_status = 'build-status-static'
                report.duration = 1
                report.save()
            else:
                # 生成报告
                _generate_allure_report(test_session)


if __name__ == '__main__':
    test_args = args_parser().parse_args()
    run_pytest_with_logger(test_args)
