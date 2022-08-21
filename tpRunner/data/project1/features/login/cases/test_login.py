#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:login_001
@time:2022/08/21
@email:tao.xu2008@outlook.com
@description:
"""
from data.project1.features.login.steps.api import login


class TestCaseLogin(object):

    def test_001(self):
        login()


if __name__ == '__main__':
    pass
