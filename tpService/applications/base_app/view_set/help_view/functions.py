#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:functions
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: pydoc生成html，再插入前端页面
"""

import os
import pydoc
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from commons.drf_base import JsonResponse
from config import root_dir


def gen_pydoc_html_content(py_path):
    """
    读取py文件生成pydoc html内容并返回
    :param py_path:
    :return:
    """
    try:
        html = pydoc.HTMLDoc()
        thing = pydoc.importfile(py_path)
        obj, name = pydoc.resolve(thing)
        page = html.page(pydoc.describe(obj), html.document(obj, name))
        return JsonResponse(page.encode(encoding='utf-8'), status=200)
    except (ImportError, pydoc.ErrorDuringImport) as e:
        print(e)
        return JsonResponse(str(e), status=200)


class BuiltinFunctionHelpViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        """生成HTML内容"""
        py_path = os.path.join(root_dir, 'core/builtin/functions.py')
        return gen_pydoc_html_content(py_path)


class CustomizedCallBackFunctionHelpViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        """自定义回调方法"""
        py_path = os.path.join(root_dir, 'customized/callback_functions.py')
        return gen_pydoc_html_content(py_path)


class CustomizedMallFunctionHelpViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        """自定义Mall方法"""
        py_path = os.path.join(root_dir, 'customized/mall_functions.py')
        return gen_pydoc_html_content(py_path)


class CustomizedSettingsFunctionHelpViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        """自定义配置中心 Settings 方法"""
        py_path = os.path.join(root_dir, 'customized/settings_functions.py')
        return gen_pydoc_html_content(py_path)


if __name__ == '__main__':
    pass
