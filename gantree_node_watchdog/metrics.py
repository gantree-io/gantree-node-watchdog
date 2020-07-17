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

