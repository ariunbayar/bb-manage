from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from conf.utils import get_setting
from .models import Repo
from .models import FetchQueue


def list(request):
    repos = Repo.objects.filter(is_watching=True).order_by('slug')
    context = {
            'last_fetch_at': get_setting('last_fetch_at', date=True),
            'repos': repos,
            'num_repos': repos.count(),
            'num_repos_hidden': Repo.objects.filter(is_watching=False).count(),
            'fetch_queue_repo_details': FetchQueue.objects.get_fetch_repo_queue(),
        }
    return render(request, 'repo/list.html', context)


def all_repos(request):
    context = {
            'repos': Repo.objects.all().order_by('slug'),
        }
    return render(request, 'repo/all_repos.html', context)


def detail(request, slug):
    repo = get_object_or_404(Repo, slug=slug)
    context = {
            'repo': repo,
            }
    return render(request, 'repo/detail.html', context)


def toggle_watching(request, slug):
    repo = get_object_or_404(Repo, slug=slug)
    repo.is_watching = not repo.is_watching
    repo.save()

    return redirect('repo-detail', repo.slug)


def fetch_all_repo(request):
    fq = FetchQueue()
    fq.fetch_type = FetchQueue.objects.FETCH_REPOSITORIES
    fq.repository = None
    fq.is_processed = False
    fq.save()
    return redirect('repo-list')


def fetch_issues(request, slug=None):
    if slug:
        repos = [get_object_or_404(Repo, slug=slug, is_watching=True)]
    else:
        repos = Repo.objects.filter(is_watching=True)

    for repo in repos:
        fq = FetchQueue()
        fq.fetch_type = FetchQueue.objects.FETCH_ISSUES
        fq.repository = repo
        fq.is_processed = False
        fq.save()

    return redirect('repo-list')
