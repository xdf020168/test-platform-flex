#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:base_models
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 基础数据表模型
"""

from django.utils import timezone
from django.db import models
# from django.contrib.auth.models import User


# 角色 选项
ROLE_CHOICES = (
    ('超级管理员', '超级管理员'),
    ('测试开发', '测试开发'),
    ('开发人员', '开发人员'),
    ('测试人员', '测试人员'),
    ('游客', '游客')
)

# 测试构建类型选项
BUILD_TYPE_CHOICE = (
    ('日构建测试', '日构建测试'),
    ('冒烟测试', '冒烟测试'),
    ('回归测试', '回归测试'),
    ('其他', '其他')
)

# 测试结果选项
TEST_RESULT_CHOICE = (
    ('', '未知'),
    ('passed', '成功'),
    ('failed', '失败'),
    ('skipped', '跳过'),
    ('error', '故障'),
)


# 重写 表数据 删除操作 - 软删除
class SoftDelTableQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_delete=True, delete_time=timezone.now())


# 重写 models.Manager，应用软删除
class BaseManager(models.Manager):
    _queryset_class = SoftDelTableQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)


# 基础数据模型：公共字段列 - 创建时间/更新时间/状态/描述
class BaseModel(models.Model):
    """公共字段列"""
    creator = models.CharField(verbose_name="创建人", max_length=20, null=True)
    updater = models.CharField(verbose_name="更新人", max_length=20, null=True)
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
    #                             verbose_name="创建人", related_name="data_creator")
    # updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
    #                             verbose_name="更新人", related_name="data_updater")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, auto_now=True)
    delete_time = models.DateTimeField(verbose_name="删除时间", null=True, default=None)
    is_delete = models.BooleanField(verbose_name='是否已删除', default=False)
    description = models.CharField(max_length=4096, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')  # 1-正常/启用； 0-异常/停用

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.delete_time = timezone.now()
        self.save()

    objects = BaseManager()

    class Meta:
        abstract = True  # 抽象基类
        verbose_name = "公共字段表"
        db_table = 'base_table'


# 字典类型表 - 灵活配置、kv存储
class DictData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', verbose_name='字典名称')
    type = models.CharField(max_length=100, default='', verbose_name='字典类型')
    remark = models.CharField(max_length=500, default='', verbose_name='备注')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '字典类型表'
        verbose_name_plural = '字典类型表'


# 部门表
class Department(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='部门名称')
    safe_name = models.SlugField(default='',  blank=True, null=True, max_length=50, verbose_name='部门标识（字母/数字）')
    leader = models.CharField(default='',  blank=True, null=True, max_length=50, verbose_name='部门负责人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


# 项目表
class Project(BaseModel):
    """项目表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='项目名称', max_length=50)
    version = models.CharField(verbose_name='项目版本', max_length=50, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


# 全局const
class GlobalConst(BaseModel):
    """全局常量const"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Name')
    value = models.TextField(blank=True, null=True, verbose_name='Value')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '全局常量'
        verbose_name_plural = '全局常量管理'


# 全局环境配置
def default_env_config():
    config = {
        "view_host": {"value": '', "description": "view host IP"},
        "base_url": {"value": '', "description": "环境base地址"},
    }
    return config


class GlobalEnv(BaseModel):
    """
    测试环境配置 environment
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    config = models.JSONField(default=default_env_config, verbose_name='环境基础配置')
    data = models.JSONField(default=dict, verbose_name='环境数据')
    mock = models.JSONField(default=dict, verbose_name='环境mock数据')
    is_mock_dynamic = models.BooleanField("是否动态更新mock", default=True)
    is_default = models.BooleanField("是否默认配置", default=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_env_config():
        return default_env_config()

    class Meta:
        verbose_name = '环境配置'
        verbose_name_plural = '环境配置管理'


# 全局标签
class GlobalLabel(BaseModel):
    """ 全局标签 """
    LABEL_TYPE_CHOICE = (
        ('priority', '优先级'),  # 如 P0、P1、P2
        ('severity', '严重等级'),  # 如 normal、blocker
        ('module', '功能特性'),  # 如 登录、权限检查
        ('stage', '测试阶段'),  # 如 冒烟测试、功能测试、集成测试、系统测试
        ('other', '其他'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='标签名')
    type = models.CharField(verbose_name='标签类型', choices=LABEL_TYPE_CHOICE, default='priority', max_length=20)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签管理'


# 测试用例集
class TestSuite(BaseModel):
    """测试用例集"""
    from django.core import serializers
    serializers.get_serializer("json")()

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='用例集')
    safe_name = models.SlugField(max_length=50, verbose_name='用例集标识（字母/数字）')
    department = models.ForeignKey(Department, verbose_name='所属部门', on_delete=models.CASCADE, null=True,
                                   related_name='suite_dept')
    labels = models.ManyToManyField(GlobalLabel, verbose_name='标签', blank=True, default=[],
                                    related_name="suite_label")

    setup = models.JSONField(blank=True, null=True, default=list, verbose_name='setup')
    setup_class = models.JSONField(blank=True, null=True, default=list, verbose_name='setup_class')
    teardown = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown')
    teardown_class = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown_class')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例集'
        verbose_name_plural = '用例集管理'


# 测试用例
class TestCase(BaseModel):
    """测试用例"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, verbose_name='用例名称')
    safe_name = models.SlugField(max_length=50, verbose_name='用例集标识（字母/数字）')
    test_suite = models.ForeignKey(TestSuite, verbose_name='所属用例集', on_delete=models.CASCADE, related_name='case_suite')
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name="case_label")
    variables = models.JSONField(default=dict, verbose_name='用例变量')
    depends = models.JSONField(default=list, verbose_name='依赖用例列表')
    result = models.CharField(verbose_name='测试结果', choices=TEST_RESULT_CHOICE, max_length=30, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '用例管理'


# 测试用例步骤
class TestStep(BaseModel):
    """
    测试用例步骤
    """
    id = models.AutoField(primary_key=True)
    sid = models.IntegerField(default=0, verbose_name='执行步骤ID')
    name = models.CharField(max_length=50, verbose_name='步骤名称')
    test_case = models.ForeignKey(TestCase, related_name='step_case', on_delete=models.CASCADE, verbose_name='所属用例')
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name='step_label')
    depends = models.ManyToManyField('self', blank=True, default=[], verbose_name='依赖项')
    skipif = models.TextField(blank=True, null=True, default='', verbose_name='skipif')  # 是否跳过步骤：条件表达式
    setup_hooks = models.JSONField(blank=True, null=True, default=list, verbose_name='setup_hooks')
    teardown_hooks = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown_hooks')
    result = models.CharField(verbose_name='测试结果', choices=TEST_RESULT_CHOICE, max_length=30, default='')

    def __unicode__(self):
        return self.description or self.name

    def __str__(self):
        return self.description or self.name

    class Meta:
        verbose_name = '测试用例步骤'
        verbose_name_plural = '测试用例步骤管理'


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


# 测试任务
class TestTask(BaseModel):
    """测试任务"""
    TAST_STATUS_CHOICE = (
        (0, '等待中'),
        (1, '运行中'),
        (2, '已完成'),
        (3, '暂停'),
        (4, '无效'),
        (5, '异常')
    )
    TEST_LEVEL_CHOICE = (
        ('test_suite', 'test_suite'),  # 查询 用例集 并执行
        ('test_case', 'test_case'),  # 查询 用例 并执行
        ('test_step', 'test_step'),  # 查询 用例步骤 并执行
    )
    # 任务 - 定时
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=100, verbose_name='名称')
    priority = models.IntegerField(default=0, verbose_name='优先级')
    cron = models.CharField(default='', max_length=100, verbose_name='cron表达式')
    status = models.SmallIntegerField(choices=TAST_STATUS_CHOICE, default=0, verbose_name='状态')
    next_run = models.CharField(blank=True, null=True, default='', max_length=50, verbose_name='下一次执行时间')
    duration = models.IntegerField(default=0, verbose_name='耗时（秒）')
    # APScheduler job state
    job_state = models.JSONField(blank=True, null=True, default=dict, verbose_name='job state')

    # 测试参数
    test_env = models.ForeignKey(GlobalEnv, verbose_name='执行环境', blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='test_env')
    test_level = models.CharField(blank=True, null=True, choices=TEST_LEVEL_CHOICE, default='test_case', max_length=20,
                                  verbose_name='测试类别')
    test_filters = models.JSONField(blank=True, null=True, default=dict, verbose_name='查询筛选器')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '测试任务'
        verbose_name_plural = '测试任务'


def default_cron_job():
    job_info = {
        "id": 0,
        "job_state": {},
        "next_run_time": ''
    }
    return job_info


# 测试环境: 验证、状态监控
class TestEnvMonitor(BaseModel):
    """测试环境监控: 日构建、环境验证、冒烟测试、业务巡检..."""
    id = models.AutoField(primary_key=True)
    env = models.ForeignKey(GlobalEnv, related_name='monitor_env', on_delete=models.CASCADE, verbose_name='被测环境')
    cron = models.CharField(default='', blank=True, null=True, max_length=100, verbose_name='cron表达式')
    cron_job = models.JSONField(default=default_cron_job, verbose_name='cron_job信息')
    build_type = models.CharField(max_length=20, choices=BUILD_TYPE_CHOICE, default='其他', verbose_name='构建类型')
    report = models.ForeignKey(TestReport, verbose_name='环境报告', blank=True, null=True, on_delete=models.CASCADE,
                               related_name='env_report')

    def __unicode__(self):
        return self.env.name

    def __str__(self):
        return self.env.name

    class Meta:
        verbose_name = '测试环境监控'
        verbose_name_plural = '测试环境监控'
