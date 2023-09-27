import json
import requests
import csv
import datetime


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
def auth_dates_collector(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    # list of source file extensions
    src_extensions = ['.java', 
                      '.kt', 
                      '.h', 
                      '.cpp', 
                      '.CMakeLists.txt'] 
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # getting the commit date
                commitDate = shaObject['commit']['author']['date']
                # Convert the commitDate to object
                commitDateObj = datetime.datetime.strptime(commitDate, "%Y-%m-%dT%H:%M:%SZ")
                # Converting UTC to PST
                commitDatePST = commitDateObj - datetime.timedelta(hours=8)
                # Formatting the PST datetime object back to a string
                formattedDate = commitDatePST.strftime("%Y-%m-%d %H:%M:%S")
                # getting the author name
                commitAuthor = shaObject['commit']['committer']['name']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename.endswith(tuple(src_extensions)): # checking if filename ends with any of the source file extensions
                        dictfiles[filename] = dictfiles.get(filename, {})
                        dictfiles[filename][commitAuthor] = formattedDate  # mapping author to date
                        print(f"Filename: {filename}, Author: {commitAuthor}, Date: {formattedDate}")

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["place-holder for token"]

dictfiles = dict()
auth_dates_collector(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/authors_and_dates_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, authors in dictfiles.items():
    for author, date in authors.items():
        rows = [filename, author, date]
        writer.writerow(rows)
fileCSV.close()

print('Finished!')
