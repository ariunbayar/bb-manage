from django.shortcuts import render, get_object_or_404, redirect
from repo.models import Repo
from repo.models import FetchQueue
from .models import Issue


def list(request):

    repos = Repo.objects.filter(sync_issues=True)
    issues = Issue.objects.all()

    context = {
            'repos': repos,
            'issues': issues,
            }
    return render(request, "issues/list.html", context)


def fetch_issues(request, slug=None):
    if slug:
        repos = [get_object_or_404(Repo, slug=slug, sync_issues=True)]
    else:
        repos = Repo.objects.filter(sync_issues=True)

    for repo in repos:
        fq = FetchQueue()
        fq.fetch_type = FetchQueue.objects.FETCH_ISSUES
        fq.repository = repo
        fq.is_processed = False
        fq.save()

    return redirect('issues-list')

