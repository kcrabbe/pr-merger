import csv
import requests
import os
from datetime import datetime

# Run command
# python3 merge_repos.py

token = 'g...31'
github_url = 'https://github.example.com/api/v3'

# runId = time as "daymonthyear hourminuteseconds"
runId = datetime.now().strftime("%d%m%Y %H%M%S")

match_string = 'CAKE-211: Adds a v2.1 Service Catalog file.'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def merge_pull_requests(owner, repo):
    print(f'\n========={repo}============\nAttempting to merge pull requests in repo {repo}')

    CONST_GETPULLS_URL = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    response = requests.get(CONST_GETPULLS_URL, headers=headers)
    foundPr = False

    if response.status_code != 200:
        write_notfound_pulls_to_csv(repo, f'Error getting pulls with code {response.status_code}')
        return

    pulls = response.json()
    for pull in pulls:
        if match_string in pull['title']:
            foundPr = True
            pull_number = pull['number']
            CONST_MERGE_URL = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/merge'
            print("Merging pull request number ", pull_number, " in repo ", repo)

            merge_response = requests.put(CONST_MERGE_URL, headers=headers)
            if merge_response.status_code == 200:
                write_merged_pulls_to_csv(repo, pull_number)
            else:
                if merge_response.status_code == 404:
                    write_notfound_pulls_to_csv(repo, f'Failed to merge pull number {pull_number} with code {merge_response.status_code}')
    
    if not foundPr:
        write_notfound_pulls_to_csv(repo, "No pulls matching string found")
def read_csv_and_merge_pulls(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            repo = row[0]
            merge_pull_requests('fanduel', repo)

def write_notfound_pulls_to_csv(repo, errorCode):
    file = f'{runId}/notfound_pulls.csv'
    print(f'Failed to get pull requests from repo {repo} with code {errorCode}')
    write_csv_file(file, [repo, errorCode])

def write_unmerged_pulls_to_csv(repo, pull_number, errorCode):
    file = f'{runId}/unmerged_pulls.csv'
    print(f'Failed to merge pull request number {pull_number} in repo {repo} with error code {errorCode}')
    write_csv_file(file, [repo, errorCode])

def write_merged_pulls_to_csv(repo, prNumber):
    file = f'{runId}/merged_pulls.csv'
    prUrl = f'https://github.com/fanduel/{repo}/pull/{prNumber}'
    print(f'Merged pull request number {prNumber} in repo {repo}')
    write_csv_file(file, [prUrl])

def write_csv_file(csv_file, data):
    # create directory if it doesn't exist with the path of {runId}, then create the file inside of the directory
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Replace 'repos.csv' with your actual CSV file path            
read_csv_and_merge_pulls('repos.csv')