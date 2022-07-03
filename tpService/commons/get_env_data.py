#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:get_env_data
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 获取环境数据 -- TODO
"""
from loguru import logger
from applications.base_app.models import GlobalEnv


class GetEnvData(object):
    def __init__(self, env_id):
        self.env_data_id = env_id

    @classmethod
    def get_props(cls):
        return [x for x in dir(cls) if isinstance(getattr(cls, x), property)]

    @property
    def env_id(self):
        return self.env_data_id

    @property
    def session_id(self):
        return 'xxxxxxxxxx'


class ValidateSession(object):
    """校验session有效性"""
    def __init__(self, env_id):
        self.session_id = GlobalEnv.objects.get(id__exact=env_id).data.get('session_id')
        logger.warning(self.session_id)

    @property
    def login(self):
        """校验登录session有效性"""
        logger.info("{0} 校验登录session有效性 {0}".format("="*10))
        try:
            login_session = 'todo-------'
            if login_session.get('sid'):
                logger.info("校验登录session有效性 => PASS.")
                return True
            logger.info("校验登录session有效性 => FAIL，需要重新获取session_id")
            return False
        except Exception as e:
            logger.warning(e)
            logger.info("校验登录session有效性 => FAIL，需要重新获取session_id")
            return False


def update_env_data(env_id):
    vs = ValidateSession(env_id)
    if vs.session_id and vs.login:
        # 如果环境数据中login session_id有效，跳过更新
        return

    logger.info("更新测试环境env数据...")
    new_env_data = {}
    GlobalEnv.objects.filter(id__exact=env_id).update(data={})  # 先清空data，避免无效session被取到
    env_data_obj = GetEnvData(env_id)
    for k in env_data_obj.get_props():
        try:
            v = env_data_obj.__getattribute__(k)
            logger.debug("环境数据：{}:{}".format(k, v))
            new_env_data.update({k: v})
        except Exception as e:
            logger.error(e)

    # 更新data数据到env
    GlobalEnv.objects.filter(id__exact=env_id).update(data=new_env_data)
    return


if __name__ == '__main__':
    pass
