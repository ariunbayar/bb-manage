from django.db import models as m


class Repo(m.Model):
    name = m.CharField(max_length=255, unique=True)
    slug = m.CharField(max_length=255, unique=True)
    is_watching = m.BooleanField(default=False)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    deleted_at = m.DateTimeField(null=True)
    num_issues = m.IntegerField()  # TODO remove

    def get_fetch_queue(self):
        return self.fetchqueue_set.filter(is_processed=False).order_by('created_at').last()

    def get_num_open_issues(self):
        return self.issue_set.exclude(state__in=self.issue_set.STATE_CLOSED).count()


class FetchQueueManager(m.Manager):

    FETCH_ISSUES       = 'issues'
    FETCH_REPOSITORIES = 'repositories'

    def get_fetch_repo_queue(self):
        values = {
                'fetch_type': self.FETCH_REPOSITORIES,
                'is_processed': False,
                }
        return self.filter(**values).order_by('created_at').last()


class FetchQueue(m.Model):

    objects = FetchQueueManager()

    fetch_type = m.CharField(max_length=255)
    repository = m.ForeignKey(Repo, on_delete=m.PROTECT, null=True)
    is_processed = m.BooleanField(default=False)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
