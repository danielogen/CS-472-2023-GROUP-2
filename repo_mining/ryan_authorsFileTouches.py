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

    # Running lists to store information taken from repo
    fileNames = []
    authors = []
    dates = []

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
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    
                    src_file_extensions = ('.java', '.kt', '.cpp', '.c')
                    # if the file ends in one of the src file extensions
                    if filename.endswith(src_file_extensions):
                            # Get author and date committed from json object
                            jsonTemp = shaDetails['commit']['author']
                            authorname = jsonTemp['name']
                            committed = jsonTemp['date']
                            # Store
                            authors.append(authorname)
                            dates.append(committed)
                            fileNames.append(filename)

            ipage += 1

        # Add lists that were populated to the dictionary
        # so we can access information outside of function
        dictfiles['filename'] = fileNames
        dictfiles['authorname'] = authors
        dictfiles['commitdate'] = dates
        
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
lstTokens = []

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

# Create a new csv file to write to
file = repo.split('/')[1]
fileOutput = 'data/SRC_file_tracking_' + file + '.csv'
header_row = ["Filename", "Author", "TouchedOnDate"]

# Write to new csv file
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(header_row)
# Write all values from dictfiles to the csv, row by row
writer.writerows(zip(*dictfiles.values()))