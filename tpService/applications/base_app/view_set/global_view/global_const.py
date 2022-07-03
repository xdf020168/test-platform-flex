#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_const
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

from commons.drf_base import BaseViewSet
from applications.base_app.models import GlobalConst
from applications.base_app.serializers import GlobalConstSerializer
from applications.base_app.filters import GlobalConstFilter


class GlobalConstViewSet(BaseViewSet):
    serializer_class = GlobalConstSerializer
    queryset = GlobalConst.objects.all().order_by('id')
    filter_fields = ("name",)
    filterset_class = GlobalConstFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalConstSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalConstSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalConstSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
