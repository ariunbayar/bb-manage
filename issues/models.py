from django.db import models as m
from repo.models import Repo


class Issue(m.Model):
    assignee = m.CharField(max_length=255, null=True)
    state = m.CharField(max_length=255)
    title = m.CharField(max_length=1000)
    type = m.CharField(max_length=255)
    kind = m.CharField(max_length=255)
    content_raw = m.TextField()
    content_html = m.TextField()
    priority = m.CharField(max_length=255)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    deleted_at = m.DateTimeField(null=True)
    repository = m.ForeignKey(Repo, on_delete=m.PROTECT, null=True)
