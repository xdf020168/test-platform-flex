#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:serializers.py
@time:2022/06/26
@email:tao.xu2008@outlook.com
@description:
"""
from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer

from applications.base_app.serializers import ProjectSerializer
from applications.api_test.models import RequestHeader, ResponseValidate, ApiGroup, ApiInfo


class RequestHeaderSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    RequestHeader 信息序列化
    """

    class Meta:
        model = RequestHeader
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ResponseValidateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    ResponseValidate信息序列化
    """

    class Meta:
        model = ResponseValidate
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ApiGroupSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """
    project = ProjectSerializer()

    class Meta:
        model = ApiGroup
        fields = '__all__'


class ApiGroupDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """
    class Meta:
        model = ApiGroup
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ApiInfoSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project = ProjectSerializer()
    api_group = ApiGroupSerializer()
    labels = GlobalLabelSerializer(many=True, read_only=True)
    update_status_name = serializers.SerializerMethodField()
    test_case_count = serializers.SerializerMethodField()

    class Meta:
        model = ApiInfo
        fields = ('id', 'yapi_id', 'project', 'api_group', 'origin', 'name', 'http_type', 'method', 'path', 'host_tag',
                  'yapi_req_headers', 'yapi_req_params', 'yapi_req_query', 'yapi_req_body_form', 'yapi_req_body_other', 'yapi_res_body',
                  'req_headers', 'req_params', 'req_json', 'req_data', 'validator', 'update_status', 'labels',
                  'create_time', 'update_time', 'delete_time', 'is_delete', 'status', 'description',
                  'creator', 'updater', 'update_status_name', 'test_case_count')

    def get_update_status_name(self, obj):
        return obj.get_update_status_display()

    def get_test_case_count(self, obj):
        return obj.step_api.all().count()


class ApiInfoCountSerializer(serializers.ModelSerializer):
    """接口统计信息序列化"""
    api_count = serializers.SerializerMethodField()
    toUpdateApiCount = serializers.SerializerMethodField()
    toVerifyApiCount = serializers.SerializerMethodField()
    updatedApiCount = serializers.SerializerMethodField()


class ApiInfoDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    class Meta:
        model = ApiInfo
        fields = '__all__'
        list_serializer_class = BulkListSerializer


if __name__ == '__main__':
    pass
