import requests
import colorama

from .utils import printStatus, expect200

REGISTER_MESSAGE = (
    colorama.Fore.LIGHTBLUE_EX + f"Registering node... " + colorama.Style.RESET_ALL
)
SCRAPE_MESSAGE = (
    colorama.Fore.LIGHTYELLOW_EX
    + f"Waiting for a scrape request from the proxy... "
    + colorama.Style.RESET_ALL
)
METRICS_MESSAGE = (
    colorama.Fore.LIGHTYELLOW_EX
    + "Sending metrics to proxy... "
    + colorama.Style.RESET_ALL
)


class Proxy:
    def __init__(self):
        pass

proxy = Proxy()
