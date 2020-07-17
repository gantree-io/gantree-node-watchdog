"""Operations related to getting local metrics."""

import requests
import colorama

from .utils import printStatus, expect200
from .conditions import is_false

GET_MESSAGE = (
    colorama.Fore.LIGHTYELLOW_EX + f"Getting metrics... " + colorama.Style.RESET_ALL
)
ACCESSIBLE_MESSAGE = (
    colorama.Fore.LIGHTBLUE_EX
    + f"Checking local metrics server is online... "
    + colorama.Style.RESET_ALL
)

# TODO: note about not holding state
class Metrics:
    def __init__(self):
        pass

    def _get(self, hostname, timeout):
        return requests.get(f"{hostname}/metrics", timeout=timeout)

    @expect200
    @printStatus(GET_MESSAGE, fail_conditions=[is_false])
    def get(self, hostname, timeout=5):
        """Get local metrics."""
        return self._get(hostname=hostname, timeout=timeout)

metrics = Metrics()
