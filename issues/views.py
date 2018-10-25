from django.shortcuts import render
from repo.models import Repo


def list(request):
    repos = Repo.objects.filter(sync_issues=True)
    context = {
            'repos': repos,
            }
    return render(request, "issues/list.html", context)
