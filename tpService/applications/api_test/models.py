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
from django.core.validators import validate_comma_separated_integer_list

from applications.base_app.models import BaseModel, Project, GlobalLabel


# 接口变更处理进度选项
API_UPDATE_STATUS_CHOICE = (
    (0, '待处理'),
    (1, '待验证'),
    (2, '已处理')
)


# 请求Header
class RequestHeader(BaseModel):
    """请求头"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, verbose_name="名称")
    value = models.TextField(blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


# 通用校验规则配置
class ResponseValidate(BaseModel):
    """ 校验规则 """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, default='默认校验', verbose_name="名称")
    check_status_code = models.BooleanField(default=True, verbose_name='检查状态代码')
    check_json_schema = models.BooleanField(default=True, verbose_name='检查json-schema')
    check_response_data = models.BooleanField(default=True, verbose_name='检查响应数据')
    status_code = models.CharField(default='200', max_length=500, verbose_name='期望状态代码',
                                   validators=[validate_comma_separated_integer_list])
    is_default = models.BooleanField("默认配置", default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                ResponseValidate.objects.filter(is_default=True).update(is_default=False)
            except ResponseValidate.DoesNotExist:
                pass
        super(ResponseValidate, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '通用校验规则配置'
        verbose_name_plural = '通用校验规则配置管理'


# 接口分组
class ApiGroup(BaseModel):
    """ 接口分组 """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='分组名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'


# 接口信息
class ApiInfo(BaseModel):
    """
    接口信息
    """
    HTTP_CHOICE = (
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS')
    )
    REQUEST_TYPE_CHOICE = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('CALL', 'CALL')
    )
    ENDPOINT_CHOICE = (
        ('mgr', '管理网络'),
        ('business', '业务网络'),
    )
    # 接口数据来源，默认manual - 手动添加
    ORIGIN_CHOICE = (
        ('xmind', 'xmind'),
        ('excel', 'excel'),
        ('manual', 'manual'),  # 默认
    )

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='project_api', null=True, on_delete=models.CASCADE, verbose_name='所属项目')
    api_group = models.ForeignKey(ApiGroup, blank=True, null=True, related_name='api_group', on_delete=models.SET_NULL, verbose_name='接口分组')
    origin = models.CharField(max_length=50, default='manual', verbose_name='接口数据来源', choices=ORIGIN_CHOICE)
    name = models.CharField(max_length=500, verbose_name='接口名称')
    http_type = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    endpoint = models.CharField(max_length=30, verbose_name='endpoint', default='business', choices=ENDPOINT_CHOICE)
    method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    path = models.CharField(max_length=1024, verbose_name='接口地址')
    # 接口请求、响应 参数模板
    req_headers = models.TextField(blank=True, null=True, verbose_name='请求头')  # json字符串
    req_params = models.TextField(blank=True, null=True, verbose_name='请求参数-params')  # json字符串
    req_data = models.TextField(blank=True, null=True, verbose_name='请求参数-data')  # json字符串
    req_json = models.TextField(blank=True, null=True, verbose_name='请求参数-json')  # json字符串
    validator = models.TextField(blank=True, null=True, verbose_name='响应数据验证')  # json字符串

    update_status = models.IntegerField(default=1, verbose_name="更新状态", choices=API_UPDATE_STATUS_CHOICE)
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name="api_label")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口信息'
        verbose_name_plural = '接口管理'
