from datetime import datetime
import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from conf.utils import get_setting, set_setting
from repo.models import Repo
from repo.models import FetchQueue
from issues.models import Issue, Comment


def to_date(v):
    if v:
        return datetime.strptime(v[:29] + v[30:], "%Y-%m-%dT%H:%M:%S.%f%z")
    else:
        return None


class Command(BaseCommand):

    def load_settings(self):

        self.conf_username = get_setting('username')
        if not self.conf_username:
            raise ImproperlyConfigured(f"Missing required environment variable 'username'")

        self.conf_client_key = get_setting('client_key')
        if not self.conf_client_key:
            raise ImproperlyConfigured(f"Missing required environment variable 'client_key'")

        self.conf_client_secret = get_setting('client_secret')
        if not self.conf_client_secret:
            raise ImproperlyConfigured(f"Missing required environment variable 'client_secret'")

        self.conf_code = get_setting('code')
        if not self.conf_code:
            raise ImproperlyConfigured(f"Missing required environment variable 'code'")

        self.conf_refresh_token = get_setting('refresh_token')
        if not self.conf_refresh_token:
            raise ImproperlyConfigured(f"Missing required environment variable 'refresh_token'")

        self.conf_access_token = get_setting('access_token')
        if not self.conf_access_token:
            raise ImproperlyConfigured(f"Missing required environment variable 'access_token'")

    def refresh_token(self):
        print('Refreshing access token...')

        data = {
                "grant_type": "refresh_token",
                "refresh_token": self.conf_refresh_token,
                }
        url = 'https://bitbucket.org/site/oauth2/access_token'
        auth = (self.conf_client_key, self.conf_client_secret)
        r = requests.post(url, auth=auth, data=data)
        if r.status_code != requests.codes.ok:
            raise Exception('Response code: %s\n%s' % (r.status_code, r.text))

        # update access_token
        access_token = r.json().get('access_token')
        set_setting('access_token', access_token)
        self.conf_access_token = access_token

        # update refresh_token
        refresh_token = r.json().get('refresh_token')
        set_setting('refresh_token', refresh_token)
        self.conf_refresh_token = refresh_token

    def load_url(self, url):

        print('loading url: %s' % url)

        headers = {'Authorization': 'Bearer ' + self.conf_access_token}
        r = requests.get(url, headers=headers)

        if r.status_code == requests.codes.unauthorized:

            self.refresh_token()

            # retry at once
            headers = {'Authorization': 'Bearer ' + self.conf_access_token}
            r = requests.get(url, headers=headers)

        if r.status_code != requests.codes.ok:
            # enough is enough, fail when we have a chance
            raise Exception('Response code: %s\n%s' % (r.status_code, r.text))

        return r.json()

    def fetch_repos(self):

        print('fetching repositories')

        url = 'https://api.bitbucket.org/2.0/repositories/%s' % self.conf_username

        num_repos = 0
        while url:
            rsp = self.load_url(url)
            for values in rsp.get('values', []):
                num_repos += 1
                repo = Repo.objects.filter(slug=values.get('slug')).last()
                if not repo:
                    repo = Repo()
                    repo.slug = values.get('slug')
                repo.name = values.get('name')
                repo.save()
            url = rsp.get('next')

        print('finished fetching %s repo details. ' % num_repos)

    def fetch_comments(self, repo, issue):

        url = 'https://api.bitbucket.org/2.0/repositories/%s/%s/issues/%s/comments' % (self.conf_username, repo.slug, issue.issue_id)
        while url:
            rsp = self.load_url(url)

            for values in rsp.get('values', []):

                import pprint; pprint.pprint(values)

                comment = Comment.objects.filter(comment_id=values.get('id')).last()
                save_required = False

                if not comment:
                    comment = Comment()
                    comment.comment_id = values.get('id')
                    save_required = True
                elif values.get('updated_on'):
                    if comment.updated_at_bb != to_date(values.get('updated_on')):
                        save_required = True

                if save_required:
                    comment.content_raw = values.get('content', {}).get('raw')
                    comment.content_html = values.get('content', {}).get('html')
                    comment.user = values.get('user', {}).get('username')
                    comment.created_at_bb = to_date(values['created_on'])
                    comment.updated_at_bb = to_date(values['updated_on']) if values['updated_on'] else None
                    comment.issue = issue
                    comment.save()

            url = rsp.get('next')

    def fetch_issues(self, repo):
        assert isinstance(repo, Repo), "Invalid repo given to fetch %r" % repo

        print('fetching issues for %s (%s)' % (repo.name, repo.slug))

        url = 'https://api.bitbucket.org/2.0/repositories/%s/%s/issues/' % (self.conf_username, repo.slug)

        num_issues = 0
        while url:
            rsp = self.load_url(url)
            for values in rsp.get('values', []):
                num_issues += 1
                issue = Issue.objects.filter(repository=repo, issue_id=values.get('id')).last() or Issue()
                if issue.updated_at_bb != to_date(values['updated_on']):
                    issue.issue_id = int(values.get('id'))
                    issue.repository = repo
                    issue.assignee = values.get('assignee', {}).get('username') if values.get('assignee') else None
                    issue.reporter = values.get('reporter', {}).get('username') if values.get('reporter') else None
                    issue.state = values.get('state')
                    issue.title = values.get('title')
                    issue.type = values.get('type')
                    issue.kind = values.get('kind')
                    issue.content_raw = values.get('content', {}).get('raw')
                    issue.content_html = values.get('content', {}).get('html')
                    issue.priority = values.get('priority')
                    issue.created_at_bb = to_date(values['created_on'])
                    issue.updated_at_bb = to_date(values['updated_on'])
                    issue.save()

                    self.fetch_comments(repo, issue)

            url = rsp.get('next')

        repo.num_issues = num_issues
        repo.save()

        print('finished fetching %s issues for %s (%s). ' % (num_issues, repo.name, repo.slug))

    def handle(self, *args, **options):

        self.load_settings()

        items = FetchQueue.objects.filter(is_processed=False).order_by('-created_at')
        if items.count() == 0:
            return

        last_fetch_date = get_setting('last_fetch_at', date=True)
        if last_fetch_date:
            print('last fetch is at: %s' % last_fetch_date.strftime(settings.DATETIME_FORMAT))

        is_repos_fetched = False
        issues_fetched_repos = []

        for item in items:
            if item.fetch_type == FetchQueue.objects.FETCH_ISSUES and item.repository.slug not in issues_fetched_repos:
                self.fetch_issues(item.repository)
                issues_fetched_repos.append(item.repository.slug)
            if item.fetch_type == FetchQueue.objects.FETCH_REPOSITORIES and not is_repos_fetched:
                self.fetch_repos()
                is_repos_fetched = True
            item.is_processed = True
            item.save()

        set_setting('last_fetch_at', datetime.now())
