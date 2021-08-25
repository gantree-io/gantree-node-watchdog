"""Module for fetching metrics."""

import requests

# import colorama
from typing import Union

from .utils import printStatus, expect200
from .conditions import is_false

GET_MESSAGE = (
    # colorama.Fore.LIGHTYELLOW_EX +  # TEMP: DISABLE COLOR
    "Getting metrics... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)
ACCESSIBLE_MESSAGE = (
    # colorama.Fore.LIGHTBLUE_EX +  # TEMP: DISABLE COLOR
    "Checking local metrics server is online... "
    # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
)

# TODO: note about not holding state
class Metrics:
    """Abstraction of metrics server.
    
    Class Should not hold any state.
    """

    def __init__(self):
        """See class docstring."""
        pass

    def _get(self, host, timeout):
        try:
            return requests.get(f"{host}/metrics", timeout=timeout)
        except Exception as e:
            return e

    @printStatus(GET_MESSAGE)
    @expect200()
    def get(self, host, timeout=5):
        """Get local metrics."""
        return self._get(host=host, timeout=timeout)

    @printStatus(ACCESSIBLE_MESSAGE, fail_conditions=[is_false])
    def accessible(self, host, timeout) -> Union[bool, Exception]:
        """Return True if local metrics can be fetched."""
        metrics = self._get(host=host, timeout=timeout)

        if isinstance(metrics, Exception):
            return metrics

        is_accessible = metrics.ok and len(metrics.content.decode("utf-8")) > 0

        return True if is_accessible else False


metrics = Metrics()
