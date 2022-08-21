#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py
@time:2022/06/25
@email:tao.xu2008@outlook.com
@description:
"""
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.extend(
    [
        root_dir,
        os.path.join(root_dir, 'tpRunner'),
        os.path.join(root_dir, 'tpService'),
        os.path.join(root_dir, 'tpService/tpService')
    ]
)


if __name__ == '__main__':
    pass
