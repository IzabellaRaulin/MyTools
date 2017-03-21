import requests.auth
import json
import sys

org_url = 'https://api.github.com/orgs/' + sys.argv[1] + '/repos?page=1&per_page=100'
user = sys.argv[2]
pw = sys.argv[3]
r = requests.get(org_url, auth=(user, pw))
repos = json.loads(r.text)
for repo in repos:
    if 'collector' in repo['name']:
        repo_data = requests.get(
            'https://api.github.com/repos/' + sys.argv[1] + '/' + repo['name'] + '/git/trees/master?recursive=1', auth=(user, pw))
        files = json.loads(repo_data.text)
        for fil in files['tree']:
            if '.md' in fil['path'] and not '.git' in fil['path']:
                md_file = requests.get(
                    'https://api.github.com/repos/' + sys.argv[1] + '/' + repo['name'] + '/contents/' + fil['path'], auth=(user, pw))
                cont = requests.get(json.loads(md_file.text)['download_url'])
                contents = cont.text.split('\n')
                print(repo['name'])
                for line in contents:
                    if '|' in line and '/intel/' in line:
                        print(line)
