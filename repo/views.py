from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from conf.utils import get_setting
from .models import Repo
from .models import FetchQueue


def list(request):
    context = {
            'last_fetch_at': get_setting('last_fetch_at', date=True),
            'repos': Repo.objects.all().order_by('slug'),
            'fetch_queue': FetchQueue.objects.get_fetch_repo_queue(),
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


@require_POST
def fetch(request):
    fq = FetchQueue()
    fq.fetch_type = FetchQueue.objects.FETCH_REPOSITORIES
    fq.repository = None
    fq.is_processed = False
    fq.save()
    return redirect('repo-list')
