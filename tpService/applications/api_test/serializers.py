#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:serializers.py
@time:2022/06/26
@email:tao.xu2008@outlook.com
@description:
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from rest_framework.authtoken.models import Token

from applications.api_test.models import Project, GlobalEnv, TestReport


class TokenSerializer(serializers.ModelSerializer):
    """
    用户信息序列化
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.user.phone")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.CharField(source="user.date_joined")

    class Meta:
        model = Token
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'phone', 'email', 'key', 'date_joined')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    # department = DepartmentSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    toUpdateApiCount = serializers.SerializerMethodField()
    toVerifyApiCount = serializers.SerializerMethodField()
    updatedApiCount = serializers.SerializerMethodField()
    apiCount = serializers.SerializerMethodField()
    apiNoCaseCount = serializers.SerializerMethodField()
    apiCoverage = serializers.SerializerMethodField()
    apiPassRate = serializers.SerializerMethodField()
    stepCount = serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    # department = DepartmentSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'department',
                  'create_time', 'update_time', 'delete_time', 'is_delete', 'status', 'description',
                  'creator', 'updater', 'apiCount', 'apiNoCaseCount', 'apiCoverage', 'stepCount',
                  'apiPassRate', 'toUpdateApiCount', 'toVerifyApiCount', 'updatedApiCount',
                  'dynamicCount', 'memberCount')

    def get_apiCount(self, obj):
        return obj.api_project.filter(status__exact=True).count()

    def get_apiNoCaseCount(self, obj):
        api_no_case_count = 0
        for api in obj.api_project.filter(status__exact=True):
            steps = api.step_api.filter(status__exact=True)
            if steps.count() == 0:
                # 接口无测试步骤
                api_no_case_count += 1
        return api_no_case_count

    def get_apiPassCount(self, obj):
        api_pass_count = 0
        for api in obj.api_project.filter(status__exact=True):
            steps = api.step_api.filter(status__exact=True)
            if steps.count() == 0:
                # 接口无测试步骤
                continue
            fail_steps = steps.exclude(result__exact='passed')
            if fail_steps.count() == 0:
                # 步骤全部通过
                api_pass_count += 1
        return api_pass_count

    def get_apiPassRate(self, obj):
        api_count = self.get_apiCount(obj)
        if api_count == 0:
            return 1
        pass_count = self.get_apiPassCount(obj)
        return round(pass_count / api_count, 3)

    def get_apiCoverage(self, obj):
        api_count = obj.api_project.filter(status__exact=True).count()
        if api_count == 0:
            return 1

        api_count_with_case = 0
        for api in obj.api_project.filter(status__exact=True):
            if api.step_api.filter(status__exact=True).count() > 0:
                api_count_with_case += 1
        return round(api_count_with_case/api_count, 3)

    def get_toUpdateApiCount(self, obj):
        to_update_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if update_status_list and min(update_status_list) == 0:
                to_update_api_count += 1
        return to_update_api_count
        # return obj.api_project.filter(update_status__exact=0, status__exact=True).count()

    def get_toVerifyApiCount(self, obj):
        to_verify_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if update_status_list and min(update_status_list) == 1:
                to_verify_api_count += 1
        return to_verify_api_count
        # return obj.api_project.filter(update_status__exact=1, status__exact=True).count()

    def get_updatedApiCount(self, obj):
        updated_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if not update_status_list or min(update_status_list) == 2:
                updated_api_count += 1
        return updated_api_count
        # return obj.api_project.filter(update_status__exact=2, status__exact=True).count()

    def get_stepCount(self, obj):
        # return obj.case_project.filter(status__exact=True).count()
        case_count = 0
        for api in obj.api_project.filter(status__exact=True):
            case_count += api.step_api.filter(status__exact=True).count()
        return case_count

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class ProjectDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    项目信息反序列化
    """
    class Meta:
        model = Project
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class GlobalEnvSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    env信息序列化
    """
    config = serializers.JSONField()
    data = serializers.JSONField()
    mock = serializers.JSONField()

    class Meta:
        model = GlobalEnv
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ApiInfoCountSerializer(serializers.ModelSerializer):
    """接口统计信息序列化"""
    api_count = serializers.SerializerMethodField()
    toUpdateApiCount = serializers.SerializerMethodField()
    toVerifyApiCount = serializers.SerializerMethodField()
    updatedApiCount = serializers.SerializerMethodField()


class TestReportSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试结果 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    env = GlobalEnvSerializer()

    class Meta:
        model = TestReport
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestReportDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试结果 反信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = TestReport
        fields = '__all__'
        list_serializer_class = BulkListSerializer


if __name__ == '__main__':
    pass
