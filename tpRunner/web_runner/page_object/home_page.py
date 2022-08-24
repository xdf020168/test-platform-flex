#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:home_page
@time:2022/07/16
@email:tao.xu2008@outlook.com
@description:首页类
"""
from selenium.webdriver.common.by import By
from web_runner.internal.base_page import BasePage


class HomePage(BasePage):
    """首页"""
    url = ''
    search_input = (By.XPATH, 'sss')
    search_button = (By.XPATH, 'sss')

    def search_xxx(self):
        self.visit()
        self.input_(self.search_input, 'xx')
        self.click(self.search_button)


if __name__ == '__main__':
    pass
