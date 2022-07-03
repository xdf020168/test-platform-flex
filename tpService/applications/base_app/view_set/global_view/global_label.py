#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_label
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

from commons.drf_base import BaseViewSet
from applications.base_app.models import GlobalLabel
from applications.base_app.serializers import GlobalLabelSerializer
from applications.base_app.filters import GlobalLabelFilter


class GlobalLabelViewSet(BaseViewSet):
    serializer_class = GlobalLabelSerializer
    queryset = GlobalLabel.objects.all().order_by('id')
    filterset_class = GlobalLabelFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
