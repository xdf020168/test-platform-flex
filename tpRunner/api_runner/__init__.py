#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py
@time:2022/04/03
@email:tao.xu2008@outlook.com
@description:
"""
import os
import sys

from config import root_dir

import django


print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(
    [
        # root_dir,
        os.path.join(root_dir, 'tpService')
    ]
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpService.settings')
django.setup()

__version__ = "1.0.1"


if __name__ == '__main__':
    pass
