#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:gen_mock_data
@time:2022/07/03
@email:tao.xu2008@outlook.com
@description: 生成mock数据
"""
import time
import datetime
import arrow
import calendar
from faker import Faker
from loguru import logger
from applications.base_app.models import GlobalEnv


class GenMockData(object):
    """生成mock数据"""

    def __init__(self):
        self.faker = Faker(['zh_CN'])

    @classmethod
    def get_props(cls):
        return [x for x in dir(cls) if isinstance(getattr(cls, x), property)]

    @property
    def name(self):
        return "auto_" + self.faker.name()

    @property
    def name2(self):
        return "auto_" + self.faker.name()

    @property
    def phone_number(self):
        """生成手机号"""
        # second = random.choice([3, 4, 5, 7, 8])
        # third = {
        #     3: random.randint(0, 9),
        #     4: random.choice([5, 7, 9]),
        #     5: random.choice([i for i in range(10) if i != 4]),
        #     7: random.choice([i for i in range(10) if i not in [4, 9]]),
        #     8: random.randint(0, 9),
        # }[second]
        # # 最后八位数字
        # suffix = ''.join(random.sample('0123456789', 8))
        # # 拼接手机号
        # # return "1{}{}{}".format(second, third, suffix)
        return self.faker.phone_number()

    @property
    def phone_number2(self):
        """生成手机号"""
        return self.faker.phone_number()

    @property
    def city(self):
        return self.faker.city()

    @property
    def address(self):
        return self.faker.address()

    @property
    def time_stamp(self):
        return int(time.time())

    @property
    def date_now_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @property
    def datetime_now_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def datetime_now_str_m(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def date_yesterday_str(self):
        return arrow.now().shift(days=-1).format("YYYY-MM-DD")

    @property
    def date_tomorrow_str(self):
        return arrow.now().shift(days=1).format("YYYY-MM-DD")

    @property
    def date_month_ago_str(self):
        return arrow.now().shift(months=-1).format("YYYY-MM-DD")

    @property
    def date_month_ago_str_2(self):
        return arrow.now().shift(months=-1).format("YYYYMMDD")

    @property
    def date_month_after_str(self):
        return arrow.now().shift(months=1).format("YYYY-MM-DD")

    @property
    def date_month_after_str_2(self):
        return arrow.now().shift(months=1).format("YYYYMMDD")

    @property
    def last_week_date(self):
        weekday = arrow.now().shift(weeks=-1).isoweekday()  # 获取当天的一周前是星期几
        mon = arrow.now().shift(weeks=-1, days=-(weekday-1))
        sun = mon.shift(days=6)
        return mon.format("YYYY-MM-DD"), sun.format("YYYY-MM-DD")

    @property
    def last_week_monday(self):
        weekday = arrow.now().shift(weeks=-1).isoweekday()  # 获取当天的一周前是星期几
        mon = arrow.now().shift(weeks=-1, days=-(weekday - 1))
        return mon.format("YYYY-MM-DD")

    @property
    def last_week_sunday(self):
        weekday = arrow.now().shift(weeks=-1).isoweekday()  # 获取当天的一周前是星期几
        mon = arrow.now().shift(weeks=-1, days=-(weekday - 1))
        sun = mon.shift(days=6)
        return sun.format("YYYY-MM-DD")

    @property
    def last_month_date(self):
        last_month_date = arrow.now().shift(months=-1).date()
        year, month = last_month_date.year, last_month_date.month
        end = calendar.monthrange(int(year), int(month))[1]
        start_date = '%s-%s-01' % (year, month)
        end_date = '%s-%s-%s' % (year, month, end)
        return start_date, end_date

    @property
    def last_month_start_date(self):
        last_month_date = arrow.now().shift(months=-1).date()
        year, month = last_month_date.year, last_month_date.month
        start_date = '%s-%s-01' % (year, month)
        return start_date

    @property
    def last_month_end_date(self):
        last_month_date = arrow.now().shift(months=-1).date()
        year, month = last_month_date.year, last_month_date.month
        end = calendar.monthrange(int(year), int(month))[1]
        end_date = '%s-%s-%s' % (year, month, end)
        return end_date

    @property
    def end_time(self):
        t = time.time()  # 获取当前时间，单位为秒
        return int(t)

    @property
    def start_time(self):
        t = time.time()
        t2 = int(t) - 2505600  # 获取当前时间三十天前的时间，单位为秒
        return t2

    @property
    def end_time_millisecond(self):
        millisecond_t = time.time()
        return int(round(millisecond_t * 1000))  # 获取当前时间戳，单位为毫秒

    @property
    def start_time_millisecond(self):
        millisecond_t = time.time()
        millisecond_t2 = int(round(millisecond_t * 1000)) - 26784000000
        return millisecond_t2  # 获取当前时间三十天前的时间戳，单位为毫秒


def update_mock_data(env_id):
    env = GlobalEnv.objects.get(id__exact=env_id)
    if not env.mock_dynamic and env.mock:
        logger.warning("mock_dynamic=False，跳过重新生成新mock数据！")
        return

    logger.info("更新测试环境mock数据...")
    mock_data = {}
    try:
        mock = GenMockData()
    except Exception as e:
        logger.error(e)
        return
    for k in mock.get_props():
        try:
            v = mock.__getattribute__(k)
            logger.debug("生成mock数据：{}:{}".format(k, v))
            mock_data.update({k: v})
        except Exception as e:
            logger.error(e)

    # 更新mock数据到env
    GlobalEnv.objects.filter(id__exact=env_id).update(mock=mock_data)
    return


if __name__ == '__main__':
    mock1 = GenMockData()
    # print(mock.get_props())
    # for p in mock.get_props():
    #     print(mock.__getattribute__(p))
    print(mock1.address)
