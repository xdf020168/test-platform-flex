#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py
@time:2022/08/21
@email:tao.xu2008@outlook.com
@description:
"""
import os
import sys
import django
from loguru import logger

from config import root_dir

sys.path.extend(
    [
        root_dir,
        os.path.join(root_dir, 'tpService')
    ]
)

logger.info('Python %s on %s' % (sys.version, sys.platform))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpService.tpService.settings')
django.setup()


if __name__ == '__main__':
    pass
