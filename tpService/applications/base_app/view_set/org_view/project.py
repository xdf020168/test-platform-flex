#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:project
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

from commons.drf_base import BaseViewSet
from applications.base_app.models import Project
from applications.base_app.filters import ProjectFilter
from applications.base_app.serializers import ProjectSerializer, ProjectDetailSerializer, ProjectDeserializer


class ProjectViewSet(BaseViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('id')
    filterset_class = ProjectFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        self.filter_fields = ("name", "department")
        self.serializer_class = ProjectSerializer
        return super().list(request, *args, **kwargs)

    # 检索数据
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProjectDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = ProjectDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = ProjectDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ProjectDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ProjectDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = ProjectDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
