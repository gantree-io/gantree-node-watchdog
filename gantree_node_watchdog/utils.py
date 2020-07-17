"""Various misc. utilities."""
import requests
import colorama
import shutil
from typing import List, Callable

from .conditions import is_exception
from .exceptions import Expected200Error


# TODO: add coloured OK's
class printStatus:
    def __init__(
        self,
        action: str,
        on_success: str = "OK",
        on_fail: str = (
            colorama.Fore.WHITE + colorama.Back.RED + "FAIL" + colorama.Style.RESET_ALL
        ),
        on_skip: str = (colorama.Fore.YELLOW + "SKIP" + colorama.Style.RESET_ALL),
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

            for fc in self.fail_conditions:
                failed = fc(res)
                if isinstance(failed, bool):
                    if failed is True:
                        print(self.on_fail + self.suffix)
                        return res
                else:
                    print("CRIT (Invalid value returned from fail condition function)")

            for sc in self.skip_conditions:
                skip = sc(res)
                if isinstance(skip, bool):
                    if skip is True:
                        print(self.on_skip + self.suffix)
                        return res

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
                    f"Expected 200, got {res.status_code}: {res.reason}"
                    + f"\nContent: {res.content.decode('utf-8')}",
                )

        return wrapper_expect200


def ascii_splash(art, fore, back, banner=False):
    lines = art.split("\n")
    t_columns, _t_lines = shutil.get_terminal_size((80, 20))
    for line_n in range(len(lines)):
        lines[line_n] = (
            fore
            + back
            + (f"{lines[line_n]:^{t_columns}}" if banner else lines[line_n])
            + colorama.Style.RESET_ALL
        )
    return (
        (colorama.Back.LIGHTYELLOW_EX if banner else "")
        + "\n"
        + colorama.Style.RESET_ALL
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
        c_default = colorama.Fore.LIGHTBLACK_EX
        c_success = colorama.Fore.GREEN
        c_fail = colorama.Fore.RED
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
            + colorama.Style.RESET_ALL
        )
