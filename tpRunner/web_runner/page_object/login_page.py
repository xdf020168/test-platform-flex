#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:login_page
@time:2022/07/16
@email:tao.xu2008@outlook.com
@description:登录页面类
"""
from selenium.webdriver.common.by import By

from tpRunner.web_runner.internal.base_page import BasePage


class LoginPage(BasePage):
    """登录页面类"""
    # 核心元素
    url = (By.NAME, 'accounts')

    user = (By.NAME, 'user')
    password = (By.NAME, 'pwd')
    login_button = (By.XPATH, '')

    # 核心业务流程
    def login(self):
        self.visit()
        self.input_(self.user, 'user')
        self.input_(self.password, 'pwd')
        self.click(self.login_button)


if __name__ == '__main__':
    pass
