import requests
import streamlit as st


@st.cache_data()
def get_github_content(user, repo, path=''):
    url = f'https://api.github.com/repos/{user}/{repo}/contents/{path}'
    response = requests.get(url)
    return response.json()

def print_directory_structure(user, repo, path=''):
    contents = get_github_content(user, repo, path)
    for item in contents:
        if item['type'] == 'dir':
            st.write(f'Directory: {item["path"]}')
            print_directory_structure(user, repo, item['path'])
        else:
            st.write(f'File: {item["path"]}')

user = st.text_input('GitHub User:')
repo = st.text_input('GitHub Repo:')

if user and repo:
    print_directory_structure(user, repo)