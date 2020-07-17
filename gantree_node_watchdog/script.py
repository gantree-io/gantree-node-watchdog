"""Binary entry point."""

import requests
import os
import time
import colorama

from .art import gantree_art
from .environment import get_env_vars
from .metrics import metrics
from .proxy import proxy
from .utils import ascii_splash, Statistics

env = get_env_vars()


def register(hostname, api_key, project_id, ip_address):
    return requests.post(
        f"{hostname}/clientNode/register",
        headers={"Authorization": f"Api-Key {api_key}"},
        json={"projectId": project_id, "ipAddress": ip_address},
    )


def proxy_scrape(hostname, node_secret, ip_address):
    return requests.get(
        f"{hostname}/clientNode/proxyScrape",
        headers={"Authorization": f"Node-Secret {node_secret}"},
    )


def get_metrics(hostname):
    return requests.get(f"{hostname}/metrics")


def main():
    print("Hello, World!\n")

    scrape = proxy_scrape(
        hostname=env["hostname"],
        node_secret=env["node_secret"],
        ip_address=env["ip_address"],
    ).json()
    print(f"Proxy scrape response:\n{scrape}\n")

    metrics = get_metrics("http://127.0.0.1:9615").content
    print(
        f"Metrics response (first 200 characters):\n{metrics.decode('utf-8')[:200]}...\n"
    )
