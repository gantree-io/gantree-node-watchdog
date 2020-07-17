"""Binary entry point."""

import requests
import os
import time
import colorama

from .art import gantree_art
from .configuration import Configuration
from .metrics import metrics
from .proxy import proxy
from .utils import ascii_splash, Statistics

colorama.init()

config = Configuration(config_file="./.gwd_config.json")


def main():
    """Execute with runner."""
    print(
        ascii_splash(
            gantree_art, colorama.Fore.BLACK, colorama.Back.LIGHTYELLOW_EX, banner=True
        )
        + "\n"
    )

    stats = Statistics()

    print(config)

    metrics_accessible = metrics.accessible(config.metrics_hostname, timeout=10)

    if isinstance(metrics_accessible, Exception):
        print(metrics_accessible)
        raise RuntimeError(metrics_accessible)

    elif metrics_accessible is False:
        raise RuntimeError("Unable to get metrics from local machine. Exiting early.")

    registration = proxy.register(
        hostname=config.proxy_hostname,
        api_key=config.api_key,
        project_id=config.project_id,
        ip_address=config.ip_address,
        client_id="node1",  # TODO: MUST NOT BE STATIC
    )
    if isinstance(registration, Exception):
        raise registration
    elif registration.status_code == 409:
        raise RuntimeError("Node already registered.")

    print()  # newline for neatness

    while True:
        try:
            stats.print_oneline()
            print()

            # TODO: create timer decorator for this method
            scrape = proxy.scrape(
                hostname=config.proxy_hostname,
                node_secret=config.node_secret,
                ip_address=config.ip_address,
            )
            if isinstance(scrape, Exception):
                raise scrape

            read_metrics = metrics.get(config.metrics_hostname)
            if isinstance(read_metrics, Exception):
                raise read_metrics

            proxy.metrics(
                hostname=config.proxy_hostname,
                node_secret=config.node_secret,
                scrape_id=scrape.json()["scrapeId"],
                metrics_response=read_metrics.content.decode("utf-8"),
            )

            stats.success()
            print()  # newline for neatness

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            print(f"Loop failed: {repr(e)}")
            stats.fail()
            # raise e
