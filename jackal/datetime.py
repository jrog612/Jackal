import datetime
from calendar import monthrange
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone

now_date_for_test = None
now_time_for_test = None


def rel_date(day=0, month=0, year=0):
    """
    tomorrow = rel_date(day=1)
    yesterday = rel_date(day=-1)
    last_month = rel_date(month=-1)
    next_month = rel_date(month=1)
    """
    today = timezone.localdate()
    if now_date_for_test is not None and settings.DEBUG:
        today = now_date_for_test

    return today + relativedelta(days=day, months=month, year=year)


def rel_time(hour=0, minute=0, second=0):
    now = timezone.localtime()
    if now_time_for_test is not None and settings.DEBUG:
        now = now_time_for_test

    return now + timedelta(minutes=minute, hours=hour, seconds=second)


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


##### TEST Helper ####

def change_now(date=None, time=None):
    """
    Remember! This method only call in TEST Environment.
    """
    if not settings.DEBUG:
        raise EnvironmentError('You can run this method only in test')

    if date is not None:
        global now_date_for_test
        now_date_for_test = date
    if time is not None:
        global now_time_for_test
        now_time_for_test = time


def reset_now():
    if not settings.DEBUG:
        raise EnvironmentError('You can run this method only in test')

    global now_date_for_test
    global now_time_for_test
    now_date_for_test = None
    now_time_for_test = None


class InDateTime:
    def __init__(self, date=None, time=None):
        self.date = date
        self.time = time

    def __enter__(self):
        change_now(self.date, self.time)

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_now()
