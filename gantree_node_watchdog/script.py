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

colorama.init()

env = get_env_vars()


def main():
    """Execute with runner."""
    print(
        ascii_splash(
            gantree_art, colorama.Fore.BLACK, colorama.Back.LIGHTYELLOW_EX, banner=True
        )
        + "\n"
    )

    stats = Statistics()

    if metrics.accessible(env["metrics_hostname"], timeout=10) is False:
        raise RuntimeError("Unable to get metrics from local machine. Exiting early.")

    # registration = proxy.register(
    #     hostname=env["proxy_hostname"],
    #     api_key=env["api_key"],
    #     project_id=env["project_id"],
    #     ip_address=env["ip_address"],
    #     client_id="node1",  # TODO: MUST NOT BE STATIC
    # )
    # if isinstance(registration, Exception):
    #     raise registration

    print()  # newline for neatness

    while True:
        try:
            stats.print_oneline()

            # print(
            # )
            # t1 = time.time()
            scrape = proxy.scrape(
                hostname=env["proxy_hostname"],
                node_secret=env["node_secret"],
                ip_address=env["ip_address"],
            )
            # t2 = time.time()

            read_metrics = metrics.get(env["metrics_hostname"])

            proxy.metrics(
                hostname=env["proxy_hostname"],
                node_secret=env["node_secret"],
                scrape_id=scrape.json()["scrapeId"],
                metrics_response=read_metrics.content.decode("utf-8"),
            )

            stats.success()

        except Exception as e:
            print(f"Loop failed: {repr(e)}")
            stats.fail()
