import datetime

from QitianSDK import QitianManager
from SmartDjango.models import Pager

from Config.models import Config, CI

current_tz = datetime.timezone(datetime.timedelta(hours=8))


def get_time(timestamp=None):
    if timestamp is None:
        return datetime.datetime.now(tz=current_tz)
    return datetime.datetime.fromtimestamp(float(timestamp), tz=current_tz)


time_pager = Pager(compare_field='time')


def time_dictor(time):
    if isinstance(time, datetime.datetime):
        return time.timestamp()


QITIAN_APP_ID = Config.get_value_by_key(CI.QITIAN_APP_ID)
QITIAN_APP_SECRET = Config.get_value_by_key(CI.QITIAN_APP_SECRET)

SECRET_KEY = Config.get_value_by_key(CI.PROJECT_SECRET_KEY)
JWT_ENCODE_ALGO = Config.get_value_by_key(CI.JWT_ENCODE_ALGO)

qt_manager = QitianManager(QITIAN_APP_ID, QITIAN_APP_SECRET)
