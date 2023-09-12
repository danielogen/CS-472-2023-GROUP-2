import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # creat list of filename, author and date
    file = []
    author = []
    commit_date = []

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # This will work for repo = 'scottyab/rootbeer'
                    # We also ignore CMake files ('.txt') since they are considered configuration files
                    list_allowed_extension = ['.java', '.kt', '.cpp', '.c']
                    if any([filename.endswith(ext) for ext in list_allowed_extension]):
                        file.append(filename)
                         # This will collect the authors and the dates when they touched for each file
                        authornamejson = shaDetails['commit']['author']
                        authorname = authornamejson['name']
                        committed_on = authornamejson['date']

                        author.append(authorname)
                        commit_date.append(committed_on)

                        print(filename, authornamejson['name'], authornamejson['date'])
            ipage += 1

        # add collected data to dictionary 
        dictfiles['filename'] = file
        dictfiles['authorname'] = author
        dictfiles['commitdate'] = commit_date
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' 
# repo = 'k9mail/k-9'
# repo = 'mendhak/gpslogger'

lstTokens = ["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"]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)


file = repo.split('/')[1]
fileOutput = f'data/file_task2_{file}.csv'
header = ["Filename", "Author", "TouchedOn"]

with open(fileOutput, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows([*zip(*dictfiles.values())])
