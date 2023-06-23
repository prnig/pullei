# pullei
Pullei is an easy-to-use Python script that downloads the newest pull requests for nuclei templates from projectdiscovery/nuclei-templates. It helps you stay updated with the latest templates not found in the existing collection.



<img width="791" alt="image" src="https://github.com/prnig/pullei/assets/73889216/b341d83d-3b02-41a7-b32c-e6d2d6b37bfd">

## Features

- The script won't add files that are already in the original nuclei-template folder. So, your existing legit templates won't break.

- The script sets up a folder named "pullei" inside the ~/nuclei-templates directory by default. This helps keep everything organized and separate from the original templates. So, you can manage your templates easly.

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

## Note
Please be aware that all the downloaded templates were created by users and have not been validated by Project Discovery yet. As a result, there is a possibility that some templates may not work as expected.

### Disclaimer 
This repository was inspired by [newclei](https://github.com/tr3ss/newclei), a tool authored by tr3ss.
