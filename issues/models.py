from django.db import models as m
from repo.models import Repo


class IssueManager(m.Manager):

    STATE_OPEN = ['new']
    STATE_CLOSED = ['resolved', 'invalid', 'closed']


class Issue(m.Model):

    objects = IssueManager()

    issue_id = m.IntegerField()
    reporter = m.CharField(max_length=255, null=True)
    assignee = m.CharField(max_length=255, null=True)
    state = m.CharField(max_length=255)
    title = m.CharField(max_length=1000)
    type = m.CharField(max_length=255)
    kind = m.CharField(max_length=255)
    content_raw = m.TextField()
    content_html = m.TextField()
    priority = m.CharField(max_length=255)
    created_at_bb = m.DateTimeField()
    updated_at_bb = m.DateTimeField()
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    deleted_at = m.DateTimeField(null=True)
    repository = m.ForeignKey(Repo, on_delete=m.PROTECT, null=True)


class Comment(m.Model):

    comment_id = m.IntegerField()
    content_raw = m.TextField(null=True)
    content_html = m.TextField()
    user = m.CharField(max_length=255)
    issue = m.ForeignKey(Issue, on_delete=m.PROTECT, null=True)
    created_at_bb = m.DateTimeField()
    updated_at_bb = m.DateTimeField(null=True)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
