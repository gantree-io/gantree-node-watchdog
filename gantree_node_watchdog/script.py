import requests
import os

from .environment import get_env_vars

env = get_env_vars()




def get_metrics(hostname):
    return requests.get(f"{hostname}/metrics")


def main():
    print("Hello, World!")

    metrics = get_metrics("http://127.0.0.1:9615").content
    print(metrics)
