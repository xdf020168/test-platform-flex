#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:base_page
@time:2022/07/16
@email:tao.xu2008@outlook.com
@description: POM基类，提供常用函数，为页面对象类服务
selenium 常用函数：
    元素定位
    输入
    点击按钮
    访问url
    等待
    关闭
"""
import time
from selenium import webdriver


class BasePage(object):
    """POM基类"""
    driver = webdriver.Chrome()
    url = ''

    def __init__(self, driver):
        self.driver = driver

    def visit(self, url=''):
        """访问url"""
        url_ = url if url else self.url
        self.driver.get(url_)

    def find_element(self, locator):
        """
        元素定位
        :param locator: 输入元组，(By.ID, 'foo')
        :return:
        """
        element = self.driver.find_element(*locator)
        return element

    def input_(self, locator, text):
        self.find_element(locator).send_keys(text)

    def click(self, locator):
        self.find_element(locator).click()

    @staticmethod
    def wait(sec):
        """
        等待 sec秒
        :param sec:
        :return:
        """
        time.sleep(sec)

    def forward(self):
        """浏览器-前进"""
        self.driver.forward()

    def back(self):
        """浏览器-后退"""
        self.driver.back()

    def close(self):
        """关闭浏览器窗口"""

    def quit(self):
        """退出浏览器"""
        self.driver.quit()


if __name__ == '__main__':
    pass
