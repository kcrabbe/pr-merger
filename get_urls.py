import csv
import os

# Run script
# python3 get_urls.py

def write_url_csv(repo, pull_number):
    string = f'https://github.com/fanduel/{repo}/pull/{pull_number}'
    write_csv_file('urls/unowned_links.csv', [string])
    print(string)

def write_csv_file(csv_file, data):
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_csv_and_convert_to_urls(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            repo = row[0]
            errorCode = row[1]
            if "Failed to merge pull number" in errorCode:
                pull_number = errorCode.split("Failed to merge pull number ")[1].split(" with code")[0]
                write_url_csv(repo, pull_number)
            else:
                write_csv_file('unmergable_links.csv', [repo, errorCode])

read_csv_and_convert_to_urls('convert.csv')