from .models import Setting


def get_setting(key):
    setting = Setting.objects.filter(key=key).first()
    return setting and setting.value or ''


def set_setting(key, value):
    setting = Setting.objects.filter(key=key).first()
    if not setting:
        setting = Setting()
        setting.key = key
    setting.value = value
    setting.save()
