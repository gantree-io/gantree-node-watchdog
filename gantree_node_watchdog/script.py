"""Binary entry point."""

import os
import time
import threading
from queue import Queue

import requests
import colorama

from .art import gantree_art
from .configuration import Configuration
from .metrics import metrics
from .proxy import proxy
from .utils import ascii_splash, Statistics

colorama.init()

# further reading/reference:
# https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/
def scrape_loop(stats, config):
    l_scrape = (
        threading.Lock()
    )  # if necessary, would want one lock per metric server we wish to scrape from

    # function to process items in the queue
    def f_scrape(scrape):
        with l_scrape:
            print("polling for a scrape request...")
            t1 = time.time()
            scrape = (
                scrape()
            )  # reassign function variable as value return from function
            # (probably not the right way to go about it, probably assign result
            # to something else in a thread-safe way)
            t2 = time.time()
            print(f"received scrape request! ({(t2 - t1)*1000:.2f}ms)")

    # wrap scrape method so it's callable later
    def r_poll_for_scrape():
        """Return a function we can call later to poll the proxy for a scrape request."""

        def func():
            return proxy.scrape(
                hostname=config.proxy_hostname,
                node_secret=config.node_secret,
                ip_address=config.ip_address,
            )

        return func

    # the function running on each thread
    def threader(index):
        """Run this function in each thread we create."""
        while True:  # until thread killed
            print(f"[{index}]: getting a task")
            f_scrape(q.get())  # get a function from the queue and execute it
            q.task_done()  # mark the task in the queue complete
            print(f"[{index}]: task completed")

    q = Queue()

    # create x many threads
    for n in range(5):
        t = threading.Thread(target=threader, args=(n,))
        t.daemon = True
        t.start()

    # queue x many jobs
    for _job in range(10):
        q.put(r_poll_for_scrape())
        print("put a r_scrape in queue")

    q.join()
    exit()

    while True:
        try:
            stats.print_oneline()
            print()

            t_scrape = threading.Thread(target=f_scrape, args=(config))
            print("Waiting for a scrape")
            t_scrape.join()
            print("Finished scraping")
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
            # raise e


def main():
    """Execute with runner."""
    print(
        ascii_splash(
            gantree_art, colorama.Fore.BLACK, colorama.Back.LIGHTYELLOW_EX, banner=True
        )
        + "\n"
    )

    stats = Statistics()

    config = Configuration(config_file="./.gwd_config.json")

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

    print()  # newline for neatness

    scrape_loop(stats, config)
