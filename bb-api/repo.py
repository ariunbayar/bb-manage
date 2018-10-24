#!/usr/bin/env python

import requests
import sys
from datetime import datetime

from local_settings import (
        USERNAME,
        REFRESH_TOKEN,
        ACCESS_TOKEN,
        CLIENT_KEY,
        CLIENT_SECRET,
        )


def output(text, title=False):
    if title:
        print('===' * 40)

    print('    %s' % text)

    if title:
        print('===' * 40)


def refresh_token():
    output('refreshing access token', title=True)
    data = {
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            }
    r = requests.post('https://bitbucket.org/site/oauth2/access_token', auth=('TODO', 'TODO'), data=data)
    rsp = r.json()
    with open("access_token.tmp", 'w') as f:
        f.write(rsp["access_token"])
    output(r.text)


def track_response(r):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = 'output-%s.json' % now

    with open(filename, 'w') as f:
        f.write(r.text)

    return r.json().get('next')


def load_url(url):
    headers = {
            'Authorization': 'Bearer ' + ACCESS_TOKEN,
            }
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.unauthorized:
            refresh_token()
        else:
            raise Exception('Response code: %s\n%s' % (r.status_code, r.text))
    else:
        return track_response(r)


url = 'https://api.bitbucket.org/2.0/repositories/user/immigration-sms/issues/'
output('Started parsing ' + url, True)
while url:
    output("Load: %s" % url)
    url = load_url(url)
