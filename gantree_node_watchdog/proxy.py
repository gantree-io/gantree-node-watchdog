import requests
import colorama

from .conditions import is_409
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

    @printStatus(REGISTER_MESSAGE, skip_conditions=[is_409])
    @expect200(allowlist=[409])
    def register(self, hostname, api_key, project_id, ip_address, client_id):
        return requests.post(
            f"{hostname}/clientNode/register",
            headers={"Authorization": f"Api-Key {api_key}"},
            json={
                "projectId": project_id,
                "ipAddress": ip_address,
                "clientId": client_id,
            },
        )

    @printStatus(SCRAPE_MESSAGE)
    @expect200()
    def scrape(self, hostname, node_secret, ip_address):
        return requests.get(
            # f"{hostname}/clientNode/proxyScrape",
            f"{hostname}/clientNode/proxyScrape",
            headers={"Authorization": f"Node-Secret {node_secret}"},
        )

    @printStatus(METRICS_MESSAGE)
    @expect200()
    def metrics(self, hostname, node_secret, scrape_id, metrics_response):
        return requests.post(
            f"{hostname}/clientNode/proxyMetrics",
            headers={"Authorization": f"Node-Secret {node_secret}"},
            json={"scrapeId": scrape_id, "metricsResponse": metrics_response},
        )


proxy = Proxy()
