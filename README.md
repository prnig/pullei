# pullei
Pullei is an easy-to-use Python script that downloads the newest pull requests for nuclei templates from projectdiscovery/nuclei-templates. It helps you stay updated with the latest templates not found in the existing collection.

<img width="791" alt="image" src="https://github.com/prnig/pullei/assets/73889216/b341d83d-3b02-41a7-b32c-e6d2d6b37bfd">


## Usage
```python
  ❯ python3 pullie.py -h
  usage: pullie.py [-h] [--github-token GITHUB_TOKEN] [--filter-cves] [--download-directory DOWNLOAD_DIRECTORY]

    options:
    -h, --help      Shows this help message and exit
    --github-token GITHUB_TOKEN
                    GitHub token to use.
    --filter-cves         Show only CVEs
    --download-directory DOWNLOAD_DIRECTORY
                    Directory to download the templates to.
```

By default, you can make up to 60 unauthenticated requests per hour to the GitHub API. If you require a higher limit, you can use a token to increase it. 
```
pullie.py --github-token GITHUB_TOKEN
```
