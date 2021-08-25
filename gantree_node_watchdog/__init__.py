"""Gantree Node Watchdog - Node monitoring client."""

from sys import version_info

if version_info.major < 3:
    print("Error: Unsupported Python version. Please use Python 3 or above.")
    exit()

__version__ = "1.1.0rc1-DEBUG-COLOR"  # TEMP: for ascii crash debugging
__author__ = "Denver Pallis (DrTexx)"
__company__ = "Gantree"
__repository__ = "https://github.com/gantree-io/gantree-node-watchdog"
__bug_tracker__ = __repository__ + "/issues"

internal_error_message = (
    f"If you see this message, please open a new issue at {__bug_tracker__}. Thanks!"
)

from .script import main
