import datetime
import time

import pytz
from dateutil.relativedelta import relativedelta
from dse import end_month, end_week, start_week, start_month


def datetime_to_timestamp(dt, tz=None):
    """
    根据时区tz将datetime类型的UTC时间dt转换成该时区的timestamp类型
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
    根据时区tz将datetime类型的UTC时间的字符串datetime_str转换成该时区的timestamp(时间戳)
    :param datetime_str:输入的dt必须是UTC时间的字符串
    :param tz:时区
    :return:
    """
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return datetime_to_timestamp(dt, tz)


def timestamp_to_datetime(ts, tz=None):
    """
    根据时区tz将本地时间戳ts转化成datetime类型
    :param ts:ts为localstamp(本地时间戳)
    :param tz:时区
    :return:
    """
    if tz:
        return datetime.datetime.fromtimestamp(ts, pytz.timezone(tz))
    return datetime.datetime.fromtimestamp(ts)


def gen_start_dt(periods, unit='D', type='datetime'):
    """
    生成这样一天,满足该天到当前时间的天数为periods(包含当天)
    生成这样一天,满足该天是一周中的第一天,该天距离本周周数为period周(包含当周)
    生成这样一天,满足该天是一月中的第一天,该天距离本月月数为period月(包含当月)
    :param periods:生成的start到当前的天数、周数、月数
    :param unit:选择periods数是天、周、月
    :param type:返回的数据类型是datetime还是date
    :return:
    """
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    start = None

    if unit == 'D':
        start = today - datetime.timedelta(days=periods - 1)
    elif unit == 'W':
        start = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(weeks=periods - 1)
    elif unit == 'M':
        start = today.replace(day=1) - relativedelta(months=periods - 1)
    if type == 'datetime':
        return start
    elif type == 'date':
        return start.date()
    return start


def gen_time_df(periods, unit='D', start=None, type='datetime', complete=False):
    """
    生成这样时间序列
    当unit为D时，生成periods天，如果没指定start，则生成从当天计算列出之前的periods天的序列，如果指定start，则生成从start开始的periods天的序列。
    当unit为W时，生成periods天，如果没指定start，则生成从本周计算列出之前的periods周第一天的序列，如果指定start，则生成从start开始的periods周第一天的序列。
    当unit为M时，生成periods天，如果没指定start，则生成从本月计算列出之前的periods月第一天的序列，如果指定start，则生成从start开始的periods月第一天的序列。
    :param periods:选择输出时间序列的天数
    :param unit:选择时间序列生成的粒度
    :param start:指定时间序列开始的时间，默认为None
    :param complete:显示生成序列的其他全部字段
    :return:
    """
    import pandas as pd

    if not start:
        start = gen_start_dt(periods=periods, unit=unit, type=type)

    if unit == 'D':
        df = pd.DataFrame([[x] for x in pd.date_range(start, periods=periods, freq='D')], columns=['day'])

        if complete:

            df['weekday'] = df['day'].dt.dayofweek
            df['week_start'] = df.apply(lambda x: x['day'] - datetime.timedelta(days=x['weekday']), axis=1)
            df['week_end'] = df.apply(lambda x: end_week(x['day'], type=type), axis=1).astype('datetime64[ns]')

            df['month_start'] = df.apply(lambda x: x['day'].replace(day=1), axis=1)
            df['month_end'] = (df.apply(lambda x: end_month(x['day'], type=type), axis=1)).astype('datetime64[ns]')

            df['month'] = df['day'].dt.month
            df['year'] = df['day'].dt.year
            df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)

    elif unit == 'W':
        df = pd.DataFrame([[x] for x in pd.date_range(start_week(start, type=type), periods=periods, freq='7D')], columns=['week_start'])
        df['week_end'] = (df.apply(lambda x: end_week(x['week_start'], type=type), axis=1)).astype('datetime64[ns]')
        if complete:
            df['month_start'] = (df.apply(lambda x: start_month(x['week_start'], type=type), axis=1)).astype('datetime64[ns]')
            df['month_end'] = (df.apply(lambda x: end_month(x['week_start'], type=type), axis=1)).astype('datetime64[ns]')
            df['month'] = df['week_start'].dt.month
            df['year'] = df['week_start'].dt.year
            df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
            df.drop('year', axis=1, inplace=True)

    elif unit == 'M':
        df = pd.DataFrame([[start_month(start, type=type) + relativedelta(months=x)] for x in range(periods)], columns=['month_start'], dtype='datetime64[ns]')
        print(df.dtypes)
        df['month_end'] = df.apply(lambda x: end_month(x['month_start'], type=type), axis=1)
        df['month'] = df['month_start'].dt.month
        df['year'] = df['month_start'].dt.year
        df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
        df.drop('year', axis=1, inplace=True)

    else:
        raise RuntimeError

    return df
