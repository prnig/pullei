import requests
import argparse
import os
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


def fetch_files(pull_request_number, github_token):
    github_files_url = f"https://api.github.com/repos/projectdiscovery/nuclei-templates/pulls/{pull_request_number}/files"
    request_headers = {"Host": "api.github.com"}
    if github_token:
        request_headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(github_files_url, headers=request_headers)
    response.raise_for_status()

    return [file_entry["raw_url"] for file_entry in response.json()]


def file_exists_in_directory(file_name, directory):
    for root, _, files in os.walk(directory):
        if file_name in files:
            return True
    return False


def download_file(url, nuclei_templates_dir, cves_only, download_directory):
    decoded_url = unquote(url)
    file_name = os.path.basename(decoded_url)
    
    download_path = os.path.join(download_directory, "pullei")
    if "cves" in url:
        download_path = os.path.join(download_path, "cves")
    else:
        download_path = os.path.join(download_path, "other")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if cves_only and "cves" not in url:
        return

    if file_exists_in_directory(file_name, nuclei_templates_dir) or file_exists_in_directory(file_name, download_path):
        print(f"\033[93mFile {file_name} already exists. Skipping download.\033[0m")
        return
    
    file_path = os.path.join(download_path, file_name)
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"\033[92mDownloaded: {file_path}\033[0m")


def execute_script():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cves-only", action="store_true", help="Download only CVEs")
    parser.add_argument("--github-token", help="GitHub token to use.")
    parser.add_argument("--nuclei-templates-path", default=os.path.expanduser("~/nuclei-templates"), help="Path to nuclei-templates directory if it doesn't exist in the root folder (~/nuclei-templates).")
    parser.add_argument("--download-directory", default=os.path.expanduser("~/nuclei-templates"), help="Directory to manually download the templates to.")
    script_args = parser.parse_args()

    pull_request_numbers = fetch_pull_requests(script_args.github_token)

    for pull_request_number in pull_request_numbers:
        file_urls = fetch_files(pull_request_number, script_args.github_token)
        for url in file_urls:
            download_file(url, script_args.nuclei_templates_path, script_args.cves_only, script_args.download_directory)


if __name__ == "__main__":
    execute_script()
