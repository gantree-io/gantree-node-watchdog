"""Gantree Node Watchdog - Node monitoring client."""

from sys import version_info

if version_info.major < 3:
    print("Error: Unsupported Python version. Please use Python 3 or above.")
    exit()

from .script import main

__version__ = "0.2.0"
__author__ = "Denver Pallis (DrTexx)"
__company__ = "Gantree"
__repository__ = "https://github.com/gantree-io/gantree-node-watchdog"
__bug_tracker__ = __repository__ + "/issues"
