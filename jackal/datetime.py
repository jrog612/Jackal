import datetime
from calendar import monthrange
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone


def local_date(days=0, months=0, years=0, **kwargs):
    """
    This function use TIMEZONE of django settings.

    when today is 2018-01-02 # YYYY-MM-DD

    >>> local_date()
    => datetime.date(2018, 1, 2)
    >>> local_date(days=1)
    => datetime.date(2018, 1, 3)
    >>> local_date(days=-1)
    => datetime.date(2017, 1, 1)
    >>> local_date(months=-1)
    => datetime.date(2018, 12, 2)
    >>> local_date(months=1)
    => datetime.date(2018, 2, 2)
    >>> local_date(day=1)
    => datetime.date(2018, 1, 1)
    >>> local_date(day=-1)
    => datetime.date(2018, 1, 31)
    >>> local_date(day=1, months=1)
    => datetime.date(2018, 2, 1)
    >>> local_date(day=-1, months=1)
    => datetime.date(2018, 2, 28)
    >>> local_date(year=2019, month=5, day=18)
    => datetime.date(2019, 5, 18)
    >>> local_date(day=-1, months=1, days=1)
    => datetime.date(2018, 3, 1)
    """
    today = timezone.localdate()

    if kwargs.get('day') == -1:
        kwargs['day'] = get_last_day_of_month(
            today.year if kwargs.get('year') is None else kwargs.get('year'),
            today.month if kwargs.get('month') is None else kwargs.get('month')
        )

    today = today.replace(**kwargs)
    return today + relativedelta(days=days, months=months, years=years)


def local_tomorrow(today=None, skip_weekend=False):
    """
    This function almost same as local_date. But it return tomorrow of given today (or local today)
    """
    if today is None:
        today = local_date()

    add_days = 1

    if skip_weekend is True:
        if today.weekday() >= 4:
            add_days = 7 - today.weekday()

    return local_date(days=add_days, month=today.month, day=today.day, year=today.year)


def local_time(hours=0, minutes=0, seconds=0, microseconds=0, to_time=False, **kwargs):
    now = timezone.localtime().replace(**kwargs)
    now += timedelta(minutes=minutes, hours=hours, seconds=seconds, microseconds=microseconds)
    if to_time:
        return now.time()
    return now


def date_range(start, end):
    if type(start) is str:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
    if type(end) is str:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')

    step = timedelta(days=1)
    ret_list = []
    while start <= end:
        ret_list.append(start)
        start += step
    return ret_list


def get_last_day_of_month(year, month):
    return monthrange(year, month)[1]
