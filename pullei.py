import requests
import argparse
import os
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote


def fetch_pull_requests(github_token):
    pull_requests = []
    page_number = 1
    while True:
        github_url = f"https://api.github.com/repos/projectdiscovery/nuclei-templates/pulls?state=open&per_page=100&page={page_number}"
        request_headers = {"Host": "api.github.com"}
        if github_token:
            request_headers["Authorization"] = f"Bearer {github_token}"

        response = requests.get(github_url, headers=request_headers)
        response.raise_for_status()

        prs_data = response.json()
        if not prs_data:
            break

        for pull_request in prs_data:
            pull_requests.append(pull_request['number'])

        page_number += 1

    return pull_requests


def fetch_files(pull_request_number, github_token, filter_cves):
    github_files_url = f"https://api.github.com/repos/projectdiscovery/nuclei-templates/pulls/{pull_request_number}/files"
    request_headers = {"Host": "api.github.com"}
    if github_token:
        request_headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(github_files_url, headers=request_headers)
    response.raise_for_status()

    files_data = response.json()

    if filter_cves:
        return [file_entry["raw_url"] for file_entry in files_data if "cves" in file_entry["filename"]]
    else:
        return [file_entry["raw_url"] for file_entry in files_data]


def file_exists_in_directory(file_name, directory):
    for root, _, files in os.walk(directory):
        if file_name in files:
            return True
    return False


def download_file(url, download_directory):
    decoded_url = unquote(url)
    file_name = os.path.basename(decoded_url)
    
    nuclei_templates_dir = os.path.expanduser("~/nuclei-templates")
    if file_exists_in_directory(file_name, nuclei_templates_dir) or file_exists_in_directory(file_name, download_directory):
        print(f"\033[93mFile {file_name} already exists. Skipping download.\033[0m")
        return
    
    file_path = os.path.join(download_directory, file_name)
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"\033[92mDownloaded: {file_path}\033[0m")


def execute_script():
    parser = argparse.ArgumentParser()
    parser.add_argument("--github-token", help="GitHub token to use.")
    parser.add_argument("--filter-cves", action="store_true", help="Show only CVEs")
    parser.add_argument("--download-directory", default=os.path.expanduser("~/nuclei-templates/pullei"), help="Directory to download the templates to.")
    script_args = parser.parse_args()

    if not os.path.exists(script_args.download_directory):
        os.makedirs(script_args.download_directory)

    pull_request_numbers = fetch_pull_requests(script_args.github_token)

    def process_pull_request(pull_request_number):
        file_urls = fetch_files(pull_request_number, script_args.github_token, script_args.filter_cves)
        for url in file_urls:
            download_file(url, script_args.download_directory)

    with ThreadPoolExecutor() as executor:
        executor.map(process_pull_request, pull_request_numbers)


if __name__ == "__main__":
    execute_script()
