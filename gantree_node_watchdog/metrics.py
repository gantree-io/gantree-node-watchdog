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
    """Abstraction of metrics server.
    
    Class Should not hold any state.
    """

    def __init__(self):
        """See class docstring."""
        pass

    def _get(self, hostname, timeout):
        try:
            return requests.get(f"{hostname}/metrics", timeout=timeout)
        except Exception as e:
            return e

    @printStatus(GET_MESSAGE)
    @expect200
    def get(self, hostname, timeout=5):
        """Get local metrics."""
        return self._get(hostname=hostname, timeout=timeout)

    @printStatus(ACCESSIBLE_MESSAGE, fail_conditions=[is_false])
    def accessible(self, hostname, timeout) -> Union[bool, Exception]:
        """Return True if local metrics can be fetched."""
        metrics = self._get(hostname=hostname, timeout=timeout)

        if isinstance(metrics, Exception):
            return metrics

        is_accessible = metrics.ok and len(metrics.content.decode("utf-8")) > 0

        return True if is_accessible else False


metrics = Metrics()
