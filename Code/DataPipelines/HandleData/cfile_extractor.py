# -*- coding: utf-8 -*-
"""
Automatically generated file from Colaboratory for scraping GitHub repositories, 
downloading files, and managing directories and files on the local system. 
It searches for repositories based on specified topics, downloads C files from those repositories, 
and cleans up downloaded files from a specified directory.
"""

# Install the requests library if not already installed
!pip install requests

import requests  # Used for making HTTP requests to the GitHub API
import os        # Provides functions for interacting with the operating system
import re        # Facilitates regular expression operations

# GitHub API headers including authorization token and request headers
headers = {
    'Authorization': 'YOUR_GITHUB_TOKEN',
    'Accept': 'application/vnd.github.v3+json'
}

def search_repositories(query):
    """
    Searches for GitHub repositories that match a specific query.
    
    Parameters:
    - query: A string containing the search criteria.
    
    Returns:
    - A list of repositories that match the query.
    """
    url = f"https://api.github.com/search/repositories?q={query}+language:C"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print("Error:", response.status_code)
        return []

# Defining topics of interest for repository search
topics = ['digital signal processing', 'embedded graphics', 'embedded hardware', 'embedded networking', 'microcontroller architecture', 'realtime systems']

# Dictionaries to store URLs, names, and full repository data
urls = {}
names = {}
repositories = {}

# Populate the dictionaries with data from the GitHub API based on defined topics
for topic in topics:
    repositories[topic] = search_repositories(topic)
    urls[topic] = [repo['html_url'] for repo in repositories[topic]]
    names[topic] = [repo['name'] for repo in repositories[topic]]

def parse_github_url(url):
    """
    Extracts the repository owner and name from a GitHub URL.
    
    Parameters:
    - url: The full URL of a GitHub repository.
    
    Returns:
    - A tuple containing the owner and repository name.
    """
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2)
    else:
        raise ValueError("Invalid GitHub URL")

def get_repo_contents(owner, repo_name, path=''):
    """
    Retrieves the contents of a repository or directory within a repository.
    
    Parameters:
    - owner: The owner of the repository.
    - repo_name: The name of the repository.
    - path: Optional path to a specific directory within the repository.
    
    Returns:
    - The contents of the repository or specified directory.
    """
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API error: {response.status_code}")

def download_file(url, directory, filename):
    """
    Downloads a file from a given URL to a specified directory.
    
    Parameters:
    - url: The URL of the file to download.
    - directory: The directory where the file will be saved.
    - filename: The name of the file to save.
    """
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    local_filepath = os.path.join(directory, filename)  # Full path for the file
    with requests.get(url) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            f.write(r.content)  # Write the file content to disk

def traverse_and_download(owner, repo_name, directory, path='', nbmax=10):
    """
    Traverses a repository's directories and downloads C files found.
    
    Parameters:
    - owner: The owner of the repository.
    - repo_name: The name of the repository.
    - directory: The local directory to save downloaded files.
    - path: The current directory path in the repository being traversed.
    - nbmax: Maximum number of files to download.
    """
    num = 0
    contents = get_repo_contents(owner, repo_name, path)
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.c'):
            print(f"Downloading {item['name']} into {directory}...")
            download_file(item['download_url'], directory, item['name'])
            num += 1
            if num >= nbmax:
                break
        elif item['type'] == 'dir':
            traverse_and_download(owner, repo_name, directory, item['path'], nbmax)

# Example usage of the functions to search, parse URL, and download contents
# Note: These calls are commented out for demonstration purposes
# owner, repo_name = parse_github_url(urls["digital signal processing"][0])
# print(get_repo_contents(owner, repo_name))
# traverse_and_download(owner, repo_name, '.', nbmax=10)

# Deleting downloaded '.c' files from a specified directory
directory = '/content/'  # The directory from which to delete files
for filename in os.listdir(directory):
    if filename.endswith('.c'):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

# Attempting to create directories based on topics and download repository contents
try:
    for k, v in urls.items():
        directory_path = k  # Using the topic name as the directory name
        try:
            os.makedirs(directory_path, exist_ok=True)
            print(f"Directory '{directory_path}' was created successfully.")
        except OSError as error:
            print(f"Error creating directory '{directory_path}': {error}")

        for url in v:
            try:
                owner, repo_name = parse_github_url(url)
                download_directory = os.path.join('.', directory_path)
                traverse_and_download(owner, repo_name, download_directory, nbmax=10)
            except Exception as e_inner:
                print(f"Error processing repository {url}: {e_inner}")
except Exception as e:
    print(f"Error: {e}")
