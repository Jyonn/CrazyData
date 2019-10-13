import datetime

from SmartDjango.models import Pager

current_tz = datetime.timezone(datetime.timedelta(hours=8))


def get_time(timestamp=None):
    if timestamp is None:
        return datetime.datetime.now(tz=current_tz)
    return datetime.datetime.fromtimestamp(float(timestamp), tz=current_tz)


time_pager = Pager(compare_field='time')


def time_dictor(time):
    if isinstance(time, datetime.datetime):
        return time.timestamp()
