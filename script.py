# This script will add 'hacktoberfest-label'
#!/usr/bin/env python3

import os
import sys
import requests
import json

LABELS = ['help wanted', 'first-timers-only', 'up-for-grabs']
API_BASE = 'https://api.github.com/'


class GitHubAPIError(Exception):
    pass


def usage():
    print('Usage: {0} user/repo'.format(sys.argv[0]))
    print('\nThis script will add the "hacktoberfest" label to any issue that '
          'also has one of the following labels applied: {0}'.format(LABELS))
    print('\nYour GitHub API token with "public_repo" permissions must be in '
          'the "GITHUB_TOKEN" environmental variable.')
    sys.exit()


def check_hacktoberfest_label(repo, token):
    url = API_BASE + 'repos/{0}/labels/hacktoberfest'.format(repo)
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {0}'.format(token)}
    r = requests.get(url, headers=headers)

    resp = r.json()
    if r.status_code == 404:
        return False
    elif r.status_code == 200 and 'hacktoberfest' in resp['name'].lower():
        return True
    else:
        raise GitHubAPIError(resp)


def create_hacktoberfest_label(repo, token):
    url = API_BASE + 'repos/{0}/labels'.format(repo)
    payload = {'name': 'hacktoberfest', 'color': 'FF635F'}
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {0}'.format(token),
               'Content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(payload))

    resp = r.json()
    if r.status_code != 201:
        raise GitHubAPIError(resp)


def apply_hacktoberfest_label(repo, token):
    issues = get_labeled_issues(repo, token)
    payload = '["hacktoberfest"]'
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {0}'.format(token)}

    for i in issues:
        url = API_BASE + 'repos/{0}/issues/{1}/labels'.format(repo, i)
        r = requests.post(url, headers=headers, data=payload)

        resp = r.json()
        if r.status_code != 200:
            raise GitHubAPIError(resp)


def get_labeled_issues(repo, token):
    issues = []
    incomplete = True
    url = API_BASE + 'search/issues'
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {0}'.format(token)}
    for label in LABELS:
        while incomplete:
            payload = 'q=is:issue+is:open+repo:{0}+label:"{1}"'.format(repo,
                                                                       label)
            r = requests.get(url, headers=headers, params=payload)

            resp = r.json()
            if r.status_code != 200:
                raise GitHubAPIError(resp)

            for i in resp['items']:
                issue_labels = []
                n = 0
                for label in resp['items'][n]['labels']:
                    issue_labels.append(label['name'].lower())
                    n += 1
                if 'hacktoberfest' not in issue_labels:
                    issues.append(i['number'])

            if 'next' in r.links:
                url = r.links['next']['url']
            else:
                incomplete = False

    return issues


def main(repo, token):
    if not check_hacktoberfest_label(repo, token):
        create_hacktoberfest_label(repo, token)
    apply_hacktoberfest_label(repo, token)


if __name__ == "__main__":
    token = os.environ['GITHUB_TOKEN']
    if token == '' or len(sys.argv) != 2 or '/' not in sys.argv[1]:
        usage()
    main(sys.argv[1], token)
