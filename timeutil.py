import datetime
import time

import pytz
from dateutil import relativedelta


def datetime_to_timestamp(dt, tz=None):
    """
    根据时区tz将datetime类型的dt转换成该时区的timestamp类型
    :param dt: datetime时间，输入的dt必须是UTC时间
    :param tz: 时区
    :return:
    """
    if tz:
        dt = pytz.timezone(tz).localize(dt)
        return int((dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
    return int(time.mktime(dt.timetuple()))


def datetime_str_to_timestamp(datetime_str, tz=None):
    """
    根据时区tz将datetime类型的字符串datetime_str转换成该时区的timestamp(时间戳)
    :param datetime_str:必须是UTC时间字符串
    :param tz:时区
    :return:
    """
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return datetime_to_timestamp(dt, tz)


def timestamp_to_datetime(ts, tz=None):
    """
    根据时区tz将时间戳ts转化成datetime类型
    :param ts:UTC时间的时间戳
    :param tz:时区
    :return:
    """
    if tz:
        return datetime.datetime.fromtimestamp(ts, pytz.timezone(tz))
    return datetime.datetime.fromtimestamp(ts)


def gen_time_df(periods, unit='D', start=None, type='datetime', complete=False):
    """
    包括本周、本月、本天
    :param periods:往前推或者后推多少天、多少周、多少月
    :param unit:选择前、后推时间粒度
    :param start:给定开始时间。当给定开始时间时，则以给定的开始时间然后往后推多少天、多少周、多少月。当未给定开始时间时，则以此刻时间作为基础，往前推多少天、多少周、多少月。
    :param complete:显示完整的字段
    :return:
    """
    import pandas as pd

    # pd.set_option('display.max_colwidth', None)
    if not start:
        # if type == 'datetime':
        today = datetime.datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        # elif type == 'date':
        #     today = datetime.date.today()

        if unit == 'D':
            start = today - datetime.timedelta(days=periods - 1)
        elif unit == 'W':
            start = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(weeks=periods - 1)
        elif unit == 'M':
            start = today.replace(day=1) - relativedelta.relativedelta(months=periods - 1)

    if unit == 'D':
        df = pd.DataFrame([[x]
                           for x in pd.date_range(start, periods=periods, freq='D')],
                          columns=['day'])
        print(df.day.dtype)
        if complete:
            df['weekday'] = df['day'].dt.dayofweek
            df['week_start'] = df.apply(lambda x: x['day'] - datetime.timedelta(days=x['weekday']), axis=1)
            df['week_end'] = df.apply(lambda x: (x['week_start'] + datetime.timedelta(days=6))
                                      .replace(hour=23, minute=59, second=59, microsecond=0), axis=1)
            df['month_start'] = df.apply(lambda x: x['day'].replace(day=1), axis=1)
            df['month_end'] = df.apply(
                lambda x: (x['day'].replace(day=1) + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1))
                    .replace(hour=23, minute=59, second=59, microsecond=0), axis=1)
            df['month'] = df['day'].dt.month
            df['year'] = df['day'].dt.year
            df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
            # df.drop('year', axis=1, inplace=True)
        print(df.month_end.dtype)
    elif unit == 'W':
        df = pd.DataFrame([[x]
                           for x in pd.date_range(start, periods=periods, freq='W-MON')],
                          columns=['week_start'])
        df['week_end'] = df.apply(lambda x: x['week_start'] + datetime.timedelta(days=6), axis=1)
        if complete:
            df['month_start'] = df.apply(lambda x: x['week_start'].replace(day=1), axis=1)
            df['month_end'] = df.apply(
                lambda x: x['week_start'].replace(day=1) + relativedelta.relativedelta(months=1) - datetime.timedelta(
                    days=1), axis=1)
            df['month'] = df['week_start'].dt.month
            df['year'] = df['week_start'].dt.year
            df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
            df.drop('year', axis=1, inplace=True)

    elif unit == 'M':
        df = pd.DataFrame([[x]
                           for x in pd.date_range(start, periods=periods, freq='MS')],
                          columns=['month_start'])
        df['month_end'] = df.apply(
            lambda x: x['month_start'].replace(day=1) + relativedelta.relativedelta(months=1) - datetime.timedelta(
                days=1), axis=1)
        df['month'] = df['month_start'].dt.month
        df['year'] = df['month_start'].dt.year
        df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
        df.drop('year', axis=1, inplace=True)

    else:
        raise RuntimeError

    return df

# datetime.timedelta()
# from dateutil.relativedelta import relativedelta

# # 时区的概念只精确到小时，各时区的分秒是一样的
# tod = datetime.datetime.today()
# print(tod.dayofweek)
# print(tod)
# print(datetime.datetime.fromtimestamp(tod))
# print(tod.tzinfo)
#
# utc1 = pytz.timezone('UTC').localize(tod)
# print(utc1)
# utc = pytz.timezone('Asia/Chongqing').localize(tod)
# print(utc)
# print(utc1)
# datetime_to_timestamp(tod)


# b = datetime.datetime(1971, 1, 1)
# print(b)
# c = pytz.timezone('Asia/Chongqing').localize(b)
# print(c)
# print(pytz.timezone('Asia/Chongqing').localize(tod))

# a = -355377889370976896756898262599672602
# b = -a
# print(type(b))
# print(b)

last = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)-datetime.timedelta(days=2)

a = gen_time_df(15,  unit='D', start=last, complete=True)
#
print(a)
# print(type(a))


# def gen_inst_daily_index(context, periods=30, nocon=False):
#     """
#     生成所有机构每天的序列表(可设置是否包含当天,默认包含)
#     :param context:
#     :param periods: 过去多少天
#     :param nocon: 设置包不包含今天的日期，默认False为包含，True为不包含
#     :return: day(datetime)
#     """
#     if nocon:
#         pd_days_time = timeutils.gen_time_df(periods + 1, unit='D')
#         pd_days_time = pd_days_time[: -1]
#     else:
#         pd_days_time = timeutils.gen_time_df(periods, unit='D')
#
#     return pd_days_time
#
#
#
# def gen_inst_monthly_index(context, periods=12):
#     """
#     生成所有机构的月份序列表(包含当月)
#     :param context:
#     :param periods: 过去几个月
#     :return: month_start(datetime), month_end(datetime), month(int64)
#     """
#     pd_months_time = timeutils.gen_time_df(periods, unit='M')
#
#
#
# def gen_inst_weekly_index(context, periods=12, noupdate=False):
#     """
#     生成所有机构的周序列表(包含当周)
#     :param context:
#     :param periods: 过去几周
#     :return: start(过去periods周的第一天), update_start(过去一周的第一天)
#     """
#
#     pd_weeks_time = timeutils.gen_time_df(periods, unit='W')
#     start = pd_weeks_time.loc[0, 'week_start']
#     update_start = pd_weeks_time.loc[10, 'week_start']
#


# today = datetime.datetime(2019, 1, 1)
# print(today.weekday())
# today = today.replace(hour=0, minute=0, second=0, microsecond=0)
# print(today - relativedelta.relativedelta(months=1))
