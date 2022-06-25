#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:main
@time:2022/04/04
@email:tao.xu2008@outlook.com
@description: 数据表模型
"""
from django.utils import timezone
from django.db import models


# 测试构建类型选项
BUILD_TYPE_CHOICE = (
    ('日构建测试', '日构建测试'),
    ('冒烟测试', '冒烟测试'),
    ('回归测试', '回归测试'),
    ('其他', '其他')
)


class SoftDelTableQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_delete=True, delete_time=timezone.now())


class BaseManager(models.Manager):
    _queryset_class = SoftDelTableQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)


# 基础表：公共字段列 - 创建时间/更新时间/状态/描述
class BaseModel(models.Model):
    """公共字段列"""
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, auto_now=True)
    delete_time = models.DateTimeField(verbose_name="删除时间", null=True, default=None)
    is_delete = models.BooleanField(verbose_name='是否已删除', default=False)

    # creator = models.CharField(verbose_name="创建人", max_length=20, null=True)
    # updater = models.CharField(verbose_name="更新人", max_length=20, null=True)
    status = models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')
    description = models.CharField(max_length=4096, blank=True, null=True, verbose_name='描述')

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.delete_time = timezone.now()
        self.save()

    objects = BaseManager()

    class Meta:
        abstract = True  # 抽象基类
        verbose_name = "公共字段表"
        db_table = 'base_table'


class Project(BaseModel):
    """项目表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='项目名称', max_length=50)
    version = models.CharField(verbose_name='版本', max_length=50, null=True)
    creator = models.CharField(verbose_name="创建人", max_length=20, null=True)
    updater = models.CharField(verbose_name="更新人", max_length=20, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


def default_env_config():
    config = {
        "view_host": {"value": '', "description": "view host IP"},
        "base_url": {"value": '', "description": "环境base地址"},
    }
    return config


class GlobalEnv(models.Model):
    """
    测试环境配置 environment
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    config = models.JSONField(default=default_env_config, verbose_name='环境基础配置')
    data = models.JSONField(default=dict, verbose_name='环境数据')
    mock = models.JSONField(default=dict, verbose_name='环境mock数据')
    is_mock_dynamic = models.BooleanField("是否动态更新mock", default=True)
    is_default = models.BooleanField("是否默认配置", default=False)
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_default_config(self):
        return default_env_config()

    class Meta:
        verbose_name = '环境配置'
        verbose_name_plural = '环境配置管理'


# 测试报告
class TestReport(BaseModel):
    BUILD_STATUS_CHOICE = (
        ('build-status-static', '构建完成'),
        ('build-status-in-progress', '构建正在进行中')
    )
    id = models.AutoField(primary_key=True)
    # 构建信息
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    build_type = models.CharField(verbose_name='构建类型', choices=BUILD_TYPE_CHOICE, default='其他', max_length=20)
    build_status = models.CharField(verbose_name='构建状态', choices=BUILD_STATUS_CHOICE, default='build-status-in-progress', max_length=50)
    env = models.ForeignKey(GlobalEnv, blank=True, null=True, related_name='report_env', on_delete=models.CASCADE,
                            verbose_name='报告关联测试环境')
    # 结果
    status = models.BooleanField(default=True, verbose_name='状态')
    duration = models.IntegerField(default=0, verbose_name='耗时（秒）')
    # case统计
    case_total = models.IntegerField(default=0, verbose_name='用例总数')
    case_passed = models.IntegerField(default=0, verbose_name='用例成功数量')
    case_failed = models.IntegerField(default=0, verbose_name='用例失败数量')
    case_skipped = models.IntegerField(default=0, verbose_name='用例跳过数量')
    case_error = models.IntegerField(default=0, verbose_name='用例故障数量')
    case_pass_rate = models.FloatField(default=0, verbose_name='用例通过率')
    case_failed_list = models.JSONField(default=list, verbose_name='用例失败列表')
    case_error_list = models.JSONField(default=list, verbose_name='用例故障列表')
    case_skipped_list = models.JSONField(default=list, verbose_name='用例跳过列表')
    # step 统计
    step_total = models.IntegerField(default=0, verbose_name='步骤总数')
    step_passed = models.IntegerField(default=0, verbose_name='步骤成功数量')
    step_failed = models.IntegerField(default=0, verbose_name='步骤失败数量')
    step_skipped = models.IntegerField(default=0, verbose_name='步骤跳过数量')
    step_error = models.IntegerField(default=0, verbose_name='步骤故障数量')
    step_pass_rate = models.FloatField(default=0, verbose_name='步骤通过率')
    broken_apis = models.JSONField(default=list, verbose_name='阻塞接口')
    step_failed_list = models.JSONField(default=list, verbose_name='步骤失败列表')
    step_error_list = models.JSONField(default=list, verbose_name='步骤故障列表')
    step_skipped_list = models.JSONField(default=list, verbose_name='步骤跳过列表')
    # 报告、日志地址记录
    client = models.CharField(default='localhost', max_length=50, blank=True, null=True, verbose_name='测试机器Client端')
    log_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='日志文件地址')
    html_report_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='pytest-html报告地址')
    allure_xml_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='allure xml数据地址')
    allure_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='allure 报告地址')
    jenkins_job_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='jenkins job name')
    jenkins_build_number = models.IntegerField(default=0, blank=True, null=True, verbose_name='jenkins build number')

    def __unicode__(self):
        return self.status

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告'
