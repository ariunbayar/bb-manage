from django.shortcuts import render
from datetime import datetime
from conf.utils import get_setting
from .models import Repo


def list(request):
    context = {
            'last_fetch_at': get_setting('last_fetch_at', date=True),
            'repos': Repo.objects.all().order_by('slug')
        }
    return render(request, "issues/list.html", context)
