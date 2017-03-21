import requests.auth
import json
import sys
import csv
import StringIO

user = sys.argv[1]
pw = sys.argv[2]

filename = "metrics.csv"

orgIntel = {
        "orgName" : "intelsdi-x",
        "mPrefix" : "/intel/",
    }
orgStaples = {
        "orgName" : "Staples-Inc",
        "mPrefix" : "/staples/",
    }


#org_url = 'https://api.github.com/orgs/' + orgIntel['orgName'] + '/repos?page=1&per_page=100'

#r = requests.get(org_url, auth=(user, pw))
#repos = json.loads(r.text)

repos = [
    {
        "name" : "snap-plugin-collector-interface",
        "org" : orgIntel,
    },
    {
        "name": "snap-plugin-collector-iostat",
        "org" : orgIntel,
    },
    {
        "name": "snap-plugin-collector-load",
        "org" : orgIntel,
    },
    {
        "name": "snap-plugin-collector-meminfo",
        "org" : orgIntel,
    },
    {
        "name": "snap-plugin-collector-netstat",
        "org" : orgStaples,
    },
    {
        "name": "snap-plugin-collector-iiomonitor",
        "org": orgIntel,
    }

]

f = open(filename, "wb")

header = "plugin" + "|" + "ib/oob" + "|" + "plugin repo" + "|" + "plugin status" + "|" + "platform component" + "|" +  "source" + "|" + "namespace" + "|" + "Description and others"

f.write(header + "\n")
print(header)

for repo in repos:
    if 'collector' in repo['name']:
        repoAddress = "https://github.com/" + repo['org']['orgName'] + repo['name']

        pluginName = repo['name'].split("snap-plugin-collector-")[1]
        repo_data = requests.get(
            'https://api.github.com/repos/' + repo['org']['orgName'] + '/' + repo['name'] + '/git/trees/master?recursive=1', auth=(user, pw))
        files = json.loads(repo_data.text)
        for fil in files['tree']:
            if '.md' in fil['path'] and not '.git' in fil['path']:
                md_file = requests.get(
                    'https://api.github.com/repos/' + repo['org']['orgName'] + '/' + repo['name'] + '/contents/' + fil['path'], auth=(user, pw))
                cont = requests.get(json.loads(md_file.text)['download_url'])
                contents = cont.text.split('\n')
                pluginName = repo['name'].split("snap-plugin-collector-")[1]

                for line in contents:
                    if '|' in line and repo['org']['mPrefix'] in line:
                        # write entry in the following format
                        # plugin name | ib/oob | plugin repo | plugin status | platform component | source | namespace | description and others
                        entry = pluginName + "|" + "|" + repoAddress + "|" + "|" + "|" + "|" + line
                        f.write(entry + "\n")

                        # print entry also in console
                        print(entry)

f.close()

