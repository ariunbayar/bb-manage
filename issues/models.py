from django.db import models as m


class Repo(m.Model):
    name = m.CharField(max_length=255, unique=True)
    slug = m.CharField(max_length=255, unique=True)
    sync_issues = m.BooleanField(default=False)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
