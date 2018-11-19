import datetime

from dateutil.relativedelta import relativedelta

from jackal.datetime import local_date, local_time, local_tomorrow
from jackal.tests import JackalTestCase


class TestDatetime(JackalTestCase):
    def test_local_date(self):
        year = self.rd.randint(2000, 2021)
        month = self.rd.randint(1, 10)
        day = self.rd.randint(1, 26)

        d = datetime.date(day=day, month=month, year=year)

        self.assertEqual(local_date(day=day, month=month, year=year), d)
        self.assertEqual(
            local_date(day=day, month=month, year=year, days=1),
            d + datetime.timedelta(days=1)
        )
        self.assertEqual(
            local_date(day=day, month=month, year=year, days=1, months=1),
            d + relativedelta(days=1, months=1)
        )
        self.assertEqual(
            local_date(day=day, month=month, year=year, days=1, months=1, years=1),
            d + relativedelta(days=1, months=1, years=1)
        )

    def test_local_tomorrow(self):
        real_tomorrow = local_date(days=1)

        self.assertEqual(real_tomorrow, local_tomorrow())
        self.assertEqual(local_date(days=2), local_tomorrow(real_tomorrow))

        if real_tomorrow.weekday() > 4:
            self.assertEqual(local_date(days=7 - real_tomorrow.weekday()), local_tomorrow(skip_weekend=True))

    def test_local_time(self):
        hour = self.rd.randint(0, 20)
        minute = self.rd.randint(0, 50)
        second = self.rd.randint(0, 50)
        microsecond = self.rd.randint(0, 900)

        t = datetime.time(hour=hour, minute=minute, second=second, microsecond=microsecond)

        lt = local_time(hour=hour, minute=minute, second=second, microsecond=microsecond, to_time=True)
        self.assertEqual(lt, t)

        lt = local_time(hour=hour, minute=minute, second=second, microsecond=microsecond, to_time=True, hours=1)
        self.assertEqual(lt, self._time_add(t, hours=1))

        lt = local_time(hour=hour, minute=minute, second=second, microsecond=microsecond, to_time=True,
                        hours=1, minutes=1)
        self.assertEqual(lt, self._time_add(t, hours=1, minutes=1))

        lt = local_time(hour=hour, minute=minute, second=second, microsecond=microsecond, to_time=True,
                        hours=1, minutes=1, seconds=1)
        self.assertEqual(lt, self._time_add(t, hours=1, minutes=1, seconds=1))

        lt = local_time(hour=hour, minute=minute, second=second, microsecond=microsecond, to_time=True,
                        hours=1, minutes=1, seconds=1, microseconds=1)
        self.assertEqual(lt, self._time_add(t, hours=1, minutes=1, seconds=1, microseconds=1))

    def _time_add(self, t, hours=0, minutes=0, seconds=0, microseconds=0):
        result = datetime.datetime.combine(
            datetime.date(1, 1, 1), t) + datetime.timedelta(hours=hours, minutes=minutes,
                                                            microseconds=microseconds,
                                                            seconds=seconds)
        return result.time()
