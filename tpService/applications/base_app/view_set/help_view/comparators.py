#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:comparators
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description:
"""

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api_runner.internal.builtin.comparators import comparators_define
from commons.drf_base import JsonResponse


class ComparatorHelpViewSet(ListModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        data_list = []
        for idx, (method, keys, desc) in enumerate(comparators_define):
            data_list.append({
                'id': idx+1,
                'method': method,
                'keys': list(keys),
                'desc': desc,
            })

        return JsonResponse({'list': data_list}, status=200)


if __name__ == '__main__':
    pass
