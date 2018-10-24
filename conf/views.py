from django.shortcuts import render
from .models import Setting


def get_setting(key):
    settings = Setting.objects.filter(key=key)
    if settings.count() == 0:
        return ''

    return settings[0].value


def configure(request):

    context = {
            'username': get_setting('username'),
            'client_key': get_setting('client_key'),
            'client_secret': get_setting('client_secret'),
            'code': get_setting('code'),
            'refresh_token': get_setting('refresh_token'),
            'access_token': get_setting('access_token'),
        }
    return render(request, 'conf/configure.html', context)


def dummy_save():
    # TODO request parsing
    setting = Setting()
    setting.key = 'client_key'
    setting.value = 'lsdkjflskdjfklskldfjlsdkjflskdfj'
    setting.save()
    # TODO render or redirect
