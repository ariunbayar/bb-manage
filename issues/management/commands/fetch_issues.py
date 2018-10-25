from datetime import datetime
import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from conf.utils import get_setting, set_setting
from issues.models import Repo


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

        last_fetch_date = get_setting('last_fetch_at', date=True)
        if last_fetch_date:
            print('last fetch is at: %s' % last_fetch_date.strftime(settings.DATETIME_FORMAT))
        print('fetching repos...')

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

        set_setting('last_fetch_at', datetime.now())

    def handle(self, *args, **options):
        self.load_settings()
        self.fetch_repos()
