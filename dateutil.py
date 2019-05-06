"""
features(功能):返回给定时间的本周、本月、本季的开始时间与结束时间
arguments(参数):today -> 给定的时间
                type -> 返回的类型，默认为datetime

"""
import datetime
from dateutil.relativedelta import relativedelta

def start_week(today, type='datetime'):
    date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    current_week_day = date - relativedelta(days=today.weekday())
    if type == 'datetime':
        return current_week_day
    elif type == 'date':
        return current_week_day.date()


def end_week(today, type='datetime'):
    date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    delta = today.weekday() - 6
    current_week_day = date - relativedelta(days=delta)
    current_week_day_finsh = datetime.datetime(current_week_day.year, current_week_day.month, current_week_day.day, 23, 59, 59)
    if type == 'datetime':
        return current_week_day_finsh
    elif type == 'date':
        return current_week_day_finsh.date()


def start_month(today, type='datetime'):
    current_month_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0)

    if type == 'datetime':
        return current_month_day
    elif type == 'date':
        return current_month_day.date()


def end_month(today, type='datetime'):
    current_month_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0)
    one_after_month_day = current_month_day + relativedelta(months=1) - relativedelta(days=1)
    end_month_finsh = datetime.datetime(one_after_month_day.year, one_after_month_day.month, one_after_month_day.day, 23, 59, 59)
    if type == 'datetime':
        return end_month_finsh
    elif type == 'date':
        return end_month_finsh.date()


def start_quarter(today, type='datetime'):
    if today.month in (1, 2, 3):
        current_quarter_first_day = datetime.datetime(today.year, 1, 1, 0, 0, 0)
        if type == 'datetime':
            return current_quarter_first_day
        elif type == 'date':
            return current_quarter_first_day.date()
    elif today.month in (4, 5, 6):
        current_quarter_first_day = datetime.datetime(today.year, 4, 1, 0, 0, 0)
        if type == 'datetime':
            return current_quarter_first_day
        elif type == 'date':
            return current_quarter_first_day.date()
    elif today.month in (7, 8, 9):
        current_quarter_first_day = datetime.datetime(today.year, 7, 1, 0, 0, 0)
        if type == 'datetime':
            return current_quarter_first_day
        elif type == 'date':
            return current_quarter_first_day.date()
    elif today.month in (10, 11, 12):
        current_quarter_first_day = datetime.datetime(today.year, 10, 1, 0, 0, 0)
        if type == 'datetime':
            return current_quarter_first_day
        elif type == 'date':
            return current_quarter_first_day.date()
    else:
        raise Exception('error datetime!')


def end_quarter(today, type='datetime'):
    if today.month in (1, 2, 3):
        current_quarter_first_day = datetime.datetime(today.year, 1, 1, 0, 0, 0)
    elif today.month in (4, 5, 6):
        current_quarter_first_day = datetime.datetime(today.year, 4, 1, 0, 0, 0)
    elif today.month in (7, 8, 9):
        current_quarter_first_day = datetime.datetime(today.year, 7, 1, 0, 0, 0)
    elif today.month in (10, 11, 12):
        current_quarter_first_day = datetime.datetime(today.year, 10, 1, 0, 0, 0)
    else:
        print('error month!')

    end_quarter_finsh = current_quarter_first_day + relativedelta(months=3) - relativedelta(days=1)
    end_quarter_finsh = datetime.datetime(end_quarter_finsh.year, end_quarter_finsh.month, end_quarter_finsh.day, 0, 0, 0)
    if type == 'datetime':
        return end_quarter_finsh
    elif type == 'date':
        return end_quarter_finsh.date()