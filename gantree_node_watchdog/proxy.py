import requests

# import colorama

from .conditions import is_409, dash_not_ready, is_403
from .utils import printStatus, expect200

REGISTER_MESSAGE = (
    # colorama.Fore.LIGHTBLUE_EX +  # TEMP: DISABLE COLOR
    "Registering node... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)
STATUS_MESSAGE = (
    # colorama.Fore.LIGHTBLUE_EX +  # TEMP: DISABLE COLOR
    "Waiting for telemetry dashboard... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)
SCRAPE_MESSAGE = (
    # colorama.Fore.LIGHTYELLOW_EX +  # TEMP: DISABLE COLOR
    "Waiting for a scrape request from the proxy... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)
METRICS_MESSAGE = (
    # colorama.Fore.LIGHTYELLOW_EX +  # TEMP: DISABLE COLOR
    "Sending metrics to proxy... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)


class Proxy:
    def __init__(self):
        pass

    @printStatus(REGISTER_MESSAGE, skip_conditions=[is_409])
    @expect200(allowlist=[409])
    def register(self, host, api_key, project_id, ip_address, client_id, pckrc):
        json_body = {
            "projectId": project_id,
            "ipAddress": ip_address,
            "clientId": client_id,
        }
        if pckrc is not None:
            json_body["pckrc"] = pckrc

        return requests.post(
            f"{host}/clientNode/register",
            headers={"Authorization": f"Api-Key {api_key}"},
            json=json_body,
        )

    @printStatus(
        STATUS_MESSAGE, fail_conditions=[is_403], skip_conditions=[dash_not_ready]
    )
    @expect200(allowlist=[403])
    def status(self, host, node_secret):
        return requests.get(
            f"{host}/clientNetwork/status",
            headers={"Authorization": f"Node-Secret {node_secret}"},
        )

    @printStatus(SCRAPE_MESSAGE, fail_conditions=[is_403])
    @expect200(allowlist=[403])
    def scrape(self, host, node_secret, ip_address):
        return requests.get(
            # f"{host}/clientNode/proxyScrape",
            f"{host}/clientNode/proxyScrape",
            headers={"Authorization": f"Node-Secret {node_secret}"},
        )

    @printStatus(METRICS_MESSAGE)
    @expect200()
    def metrics(self, host, node_secret, scrape_id, metrics_response):
        return requests.post(
            f"{host}/clientNode/proxyMetrics",
            headers={"Authorization": f"Node-Secret {node_secret}"},
            json={"scrapeId": scrape_id, "metricsResponse": metrics_response},
        )


proxy = Proxy()
