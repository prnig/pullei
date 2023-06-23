# pullei
Pullei is an easy-to-use Python script that downloads the pull requests for nuclei templates from projectdiscovery/nuclei-templates repo. It helps you stay updated with the latest templates not found in the existing collection.


<img width="933" alt="image" src="https://github.com/prnig/pullei/assets/73889216/d61f840d-5313-434e-ad2d-aee5e184d1d1">



## Features

- The script won't add files that are already in the original nuclei-template folder. So, your existing legit templates won't break.

- The script sets up a folder named "pullei" inside the ~/nuclei-templates directory by default. This helps keep everything organized and separate from the original templates. So, you can manage your templates easily.

## Usage
```python
❯ python3 pullei.py -h
usage: pullei.py [-h] [-c] [--github-token GITHUB_TOKEN] [--nuclei-templates-path NUCLEI_TEMPLATES_PATH] [--download-directory DOWNLOAD_DIRECTORY]

options:
  -h, --help            show this help message and exit
  -c, --cves-only       Download only CVEs
  --github-token GITHUB_TOKEN
                        GitHub token to use.
  --nuclei-templates-path NUCLEI_TEMPLATES_PATH
                        Path to nuclei-templates directory if it doesn't exist in the root folder (~/nuclei-templates).
  --download-directory DOWNLOAD_DIRECTORY
                        Directory to manually download the templates to.
```

By default, you can make up to 60 unauthenticated requests per hour to the GitHub API. If you require a higher limit, you can use a token to increase it. 

```
pullei.py --github-token GITHUB_TOKEN
```

## Note
Please be aware that all the downloaded templates were created by users and have not been validated by Project Discovery yet. As a result, there is a possibility that some templates may not work as expected.

<br>
This repository was inspired by https://github.com/tr3ss/newclei, a tool authored by tr3ss.
