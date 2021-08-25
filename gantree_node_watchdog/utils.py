"""Various misc. utilities."""
import os
import sys
import shutil
import json
from pathlib import Path
from typing import List, Callable

import requests

# import colorama
from ipify import get_ip
from ipify.exceptions import ConnectionError, ServiceError

from .conditions import is_exception
from .exceptions import Expected200Error

# HACK(Denver): disables the splash, being used to debug encoding issues
HACK_splash_disabled = (
    True if os.getenv("GANTREE_NODE_WATCHDOG_DISABLE_SPLASH") != None else False
)


def get_public_ip_addr():
    """Return the public IP address of machine executing script."""
    try:
        return get_ip()
    except ConnectionError:
        print(
            "Warning: Unable to reach the ipify service."
            + " This is likely due to a network error and not the ipify service."
            + "\nWe'll try getting your public IP address from somewhere else."
        )
    except ServiceError:
        print(
            "Warning: Ipify service is experiencing issues."
            + "\nWe'll try getting your public IP address from somewhere else."
        )
    except Exception as e:
        print(
            "Warning: Failed to public IP address from ipify for unknown reasons."
            + f"\nError received: {e}"
            + "\nWe'll try getting your public IP address from somewhere else."
        )


# TODO: add coloured OK's
class printStatus:
    def __init__(
        self,
        action: str,
        on_success: str = "OK",
        on_fail: str = (
            # colorama.Fore.WHITE + colorama.Back.RED +  # TEMP: DISABLE COLOR
            "FAIL"
            # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        ),
        on_skip: str = (
            # colorama.Fore.YELLOW +  # TEMP: DISABLE COLOR
            "SKIP"
            # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        ),
        suffix: str = "",
        fail_conditions: List[Callable[[str], None]] = [],
        skip_conditions: List[Callable[[str], None]] = [],
    ):
        self.action = action
        self.on_success = on_success
        self.on_fail = on_fail
        self.on_skip = on_skip
        self.suffix = suffix
        self.fail_conditions = [is_exception, *fail_conditions]
        self.skip_conditions = [*skip_conditions]

    def __call__(self, func):
        def wrapper_printStatus(*args, **kwargs):
            print(self.action, end="", flush=True)

            res = func(*args, **kwargs)

            # TODO: address redundant code between fail/skip condition checking loops
            for fc in self.fail_conditions:
                failed = fc(res)
                failed_reason = None

                if isinstance(failed, tuple):
                    """If the fail condition returns a tuple, unpack it."""
                    if len(failed) == 2:
                        failed, failed_reason = failed

                if isinstance(failed, bool):
                    if failed is True:
                        print(
                            self.on_fail
                            + (f" ({failed_reason})" if failed_reason else "")
                            + self.suffix
                        )
                        return res
                else:
                    if isinstance(failed, Exception):
                        return failed
                    else:
                        return TypeError("Fail condition didn't return a bool")

            for sc in self.skip_conditions:
                skip = sc(res)
                skip_reason = None

                if isinstance(skip, tuple):
                    """If the skip condition returns a tuple, unpack it."""
                    if len(skip) == 2:
                        skip, skip_reason = skip

                if isinstance(skip, bool):
                    if skip is True:
                        print(
                            self.on_skip
                            + (f" ({skip_reason})" if skip_reason else "")
                            + self.suffix
                        )
                        return res
                else:
                    if isinstance(skip, Exception):
                        return skip
                    else:
                        return TypeError("Skip condition didn't return a bool")

            print(self.on_success + self.suffix)
            return res

        return wrapper_printStatus


class expect200:
    """Return runtime error if response status code isn't 200."""

    def __init__(self, allowlist=[]):
        self.allowlist = allowlist

    def __call__(self, func):
        def wrapper_expect200(*args, **kwargs):
            res = func(*args, **kwargs)
            if not isinstance(res, requests.Response):
                return TypeError(
                    f"Response instance not returned from decorated function, instead got {type(res)}"
                )
            if res.ok:
                return res
            elif res.status_code in self.allowlist:
                return res
            else:
                return Expected200Error(
                    res,
                    "Expected 200"
                    + (
                        f"/{'/'.join([str(code) for code in self.allowlist])}"
                        if self.allowlist
                        else ""
                    )
                    + f" got {res.status_code}: {res.reason}"
                    + (
                        f"\nPerhaps your hosts are misconfigured?"
                        if res.status_code == 404
                        else ""
                    )
                    + f"\nURL: {res.url}"
                    + f"\nContent: '{res.content.decode('utf-8')}'",
                )

        return wrapper_expect200


def ascii_splash(art, fore, back, banner=False):
    # HACK(Denver): disable the splash, used to debug ascii encoding crash
    if HACK_splash_disabled is True:
        return ""

    lines = art.split("\n")
    t_columns, _t_lines = shutil.get_terminal_size((80, 20))
    for line_n in range(len(lines)):
        lines[line_n] = (
            fore
            + back
            + (f"{lines[line_n]:^{t_columns}}" if banner else lines[line_n])
            # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        )
    return (
        # (colorama.Back.LIGHTYELLOW_EX if banner else "")  # TEMP: DISABLE COLOR
        "\n"
        # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
    ).join(lines)


class Statistics:
    def __init__(self):
        self.successes = 0
        self.failures = 0

    def success(self):
        self.successes += 1

    def fail(self):
        self.failures += 1

    def print_oneline(self):
        # c_default = colorama.Fore.LIGHTBLACK_EX  # TEMP: DISABLE COLOR
        c_default = ""  # TEMP: DISABLE COLOR
        # c_success = colorama.Fore.GREEN  # TEMP: DISABLE COLOR
        c_success = ""  # TEMP: DISABLE COLOR
        # c_fail = colorama.Fore.RED  # TEMP: DISABLE COLOR
        c_fail = ""  # TEMP: DISABLE COLOR
        print(
            c_default
            + "[ STATUS ] ---- [ Proxied Requests: "
            + c_success
            + str(self.successes)
            + c_default
            + " ] ---- [ Failures: "
            + c_fail
            + str(self.failures)
            + c_default
            + " ]"
            # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        )


def read_json(filepath):
    """Read a json file, return (not raise) an exception if it doesn't exist."""
    print(Path(filepath))
    if not Path(filepath).exists():
        return FileNotFoundError(f"couldn't find file '{filepath}'")

    with open(filepath, "r") as f:
        return json.load(f)


def is_terminal_interactive():
    """Check if the active terminal is interactive."""
    isatty = os.isatty(sys.stdout.fileno())
    if isinstance(isatty, bool):
        return isatty
    else:
        return RuntimeError("Expected returned value to be a boolean.")
