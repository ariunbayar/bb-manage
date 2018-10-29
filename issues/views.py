from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from repo.models import Repo
from repo.models import FetchQueue
from .models import Issue
from .forms import FilterIssuesForm


def list(request):

    issues = Issue.objects.exclude(state__in=Issue.objects.STATE_CLOSED)
    available_assignees = [v for v in issues.values_list('assignee', flat=True).distinct()]
    repo_choices = [(s, n) for s, n in issues.values_list('repository_id', 'repository__name').distinct()]

    assignee_choices = [(v, v) for v in available_assignees if v]
    if None in available_assignees:
        assignee_choices = [('', '-- empty --')] + assignee_choices
    form = FilterIssuesForm(assignee_choices, repo_choices, request.GET)

    if form.is_valid():

        if len(form.cleaned_data['assignees']):
            # filter by assignees handling the empty ones
            assignees = [v for v in form.cleaned_data['assignees'] if v]
            if '' in form.cleaned_data['assignees']:
                issues = issues.filter(Q(assignee__in=assignees) | Q(assignee__isnull=True))
            else:
                issues = issues.filter(assignee__in=assignees)

        if len(form.cleaned_data['repos']):
            # filter by repositories
            issues = issues.filter(repository__in=form.cleaned_data['repos'])

    context = {
            'issues': issues,
            'form': form,
            }
    return render(request, "issues/list.html", context)


def detail(request, slug, issue_id):
    issue = get_object_or_404(Issue, repository__slug=slug, issue_id=issue_id)

    context = {
            'issue': issue,
            'comments': issue.comment_set.order_by('created_at_bb'),
            }

    return render(request, "issues/detail.html", context)
