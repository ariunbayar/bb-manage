from django.shortcuts import render, get_object_or_404, redirect
from conf.utils import get_setting
from .models import Repo


def list(request):
    context = {
            'last_fetch_at': get_setting('last_fetch_at', date=True),
            'repos': Repo.objects.all().order_by('slug')
        }
    return render(request, 'repo/list.html', context)


def detail(request, slug):
    repo = get_object_or_404(Repo, slug=slug)
    context = {
            'repo': repo,
            }
    return render(request, 'repo/detail.html', context)


def toggle_sync_issues(request, slug):
    repo = get_object_or_404(Repo, slug=slug)
    repo.sync_issues = not repo.sync_issues
    repo.save()

    return redirect('repo-detail', repo.slug)
