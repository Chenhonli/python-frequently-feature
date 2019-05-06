import datetime
import time

import pytz
from dateutil import relativedelta


def datetime_str_to_timestamp(datetime_str, tz=None):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return datetime_to_timestamp(dt, tz)


def datetime_to_timestamp(dt, tz=None):
    if tz:
        dt = pytz.timezone(tz).localize(dt)
        return int((dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
    return int(time.mktime(dt.timetuple()))


def timestamp_to_datetime(ts, tz=None):
    if tz:
        return datetime.datetime.fromtimestamp(ts, pytz.timezone(tz))
    return datetime.datetime.fromtimestamp(ts)


def gen_time_df(periods, unit='D', start=None, complete=False):
    import pandas as pd

    if not start:
        today = datetime.date.today()
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
        if complete:
            df['weekday'] = df['day'].dt.dayofweek
            df['week_start'] = df.apply(lambda x: x['day'] - datetime.timedelta(days=x['weekday']), axis=1)
            df['week_end'] = df.apply(lambda x: x['week_start'] + datetime.timedelta(days=6), axis=1)
            df['month_start'] = df.apply(lambda x: x['day'].replace(day=1), axis=1)
            df['month_end'] = df.apply(
                lambda x: x['day'].replace(day=1) + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1),
                axis=1)
            df['month'] = df['day'].dt.month
            df['year'] = df['day'].dt.year
            df['month'] = df.apply(lambda r: int(str(r['year']) + str(r['month']).zfill(2)), axis=1)
            df.drop('year', axis=1, inplace=True)

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
