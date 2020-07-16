import requests
import os

from .environment import get_env_vars

env = get_env_vars()



def main():
    response = requests.get('http://127.0.0.1:9615/metrics')
    print(response.content)
