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
from config import root_dir

sys.path.extend(
    [
        # root_dir,
        os.path.join(root_dir, 'tpService')
    ]
)


if __name__ == '__main__':
    pass
