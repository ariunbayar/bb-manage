from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import BBSettingForm
from .models import Setting
from .utils import get_setting, set_setting


def configure(request):

    if request.method == 'POST':
        form = BBSettingForm(request.POST)
        if form.is_valid():
            set_setting('username', form.cleaned_data['username'])
            set_setting('client_key', form.cleaned_data['client_key'])
            set_setting('client_secret', form.cleaned_data['client_secret'])
            set_setting('code', form.cleaned_data['code'])
            set_setting('refresh_token', form.cleaned_data['refresh_token'])
            set_setting('access_token', form.cleaned_data['access_token'])
            return redirect('configure')
    else:
        data = {
            'username': get_setting('username'),
            'client_key': get_setting('client_key'),
            'client_secret': get_setting('client_secret'),
            'code': get_setting('code'),
            'refresh_token': get_setting('refresh_token'),
            'access_token': get_setting('access_token'),
        }
        form = BBSettingForm(initial=data)

    context = {
            'form': form,
        }
    return render(request, 'conf/configure.html', context)
