import requests
import os

from .environment import get_env_vars

env = get_env_vars()


def proxy_scrape(hostname, node_secret):
    return requests.post(
        f"{hostname}/clientNode/proxyScrape",
        headers={"Authorization": f"Node-Secret {node_secret}"},
    )


def get_metrics(hostname):
    return requests.get(f"{hostname}/metrics")


def main():
    print("Hello, World!")

    metrics = get_metrics("http://127.0.0.1:9615").content
    print(metrics)
