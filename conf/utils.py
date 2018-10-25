from django.conf import settings
from .models import Setting
import datetime


def get_setting(key, date=False):
    setting = Setting.objects.filter(key=key).first()

    if not setting:
        return ''

    if date:  # convert to datetime object
        return datetime.datetime.strptime(setting.value, settings.DATETIME_FORMAT)

    return setting.value


def set_setting(key, value, date=False):
    setting = Setting.objects.filter(key=key).first()

    if not setting:
        setting = Setting()
        setting.key = key

    if isinstance(value, datetime.datetime):
        value = value.strftime(settings.DATETIME_FORMAT)

    setting.value = value
    setting.save()
