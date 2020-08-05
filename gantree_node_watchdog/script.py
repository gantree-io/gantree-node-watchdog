"""Binary entry point."""

import os
import time

import requests
import colorama

from .art import gantree_art
from .configuration import Configuration
from .metrics import metrics
from .proxy import proxy
from .utils import ascii_splash, Statistics

colorama.init()


def main():
    """Execute with runner."""
    print(
        ascii_splash(
            gantree_art, colorama.Fore.BLACK, colorama.Back.LIGHTYELLOW_EX, banner=True
        )
        + "\n"
    )

    stats = Statistics()

    config = Configuration(config_file="./.gnw_config.json")

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
        client_id=config.client_id,
    )
    if isinstance(registration, Exception):
        raise registration
    elif registration.status_code == 409:
        # print("Node already registered.")
        pass
    else:
        reg_json = registration.json()
        config._save_registration_details(
            node_id=reg_json["nodeId"], node_secret=reg_json["nodeSecret"]
        )

    if not config._has_registration_details():
        print(
            "\n"
            + "⮞ Your node is already registered, but you don't"
            + " have a node_id and node_secret stored."
            + "\n⮞ If this is a new node, please use a different client_id."
            + "\n⮞ If this is an already registered node with the correct"
            + " client_id, please de-register and re-register it."
            + "\n⮞ For security reasons we cannot send your node_id and"
            + " node_secret again after you initially register your node."
            + "\n"
        )
        return RuntimeError(
            "Missing registration details for already registered client_id"
        )

    while True:
        try:
            proxy_status = proxy.status(
                hostname=config.proxy_hostname, node_secret=config.node_secret
            )

            if isinstance(proxy_status, Exception):
                raise proxy_status

            else:
                dashboard_status = proxy_status.json()["status"]["telemDashboard"]

                if dashboard_status == "READY":
                    break

                time.sleep(10)

        except KeyboardInterrupt:
            print("\nCancelling...")
            break

        except Exception as e:
            print(f"ERROR: {repr(e)}")
            time.sleep(0.1)

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
                print(scrape)
                raise RuntimeError(scrape)

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
            time.sleep(0.1)
            # raise e
