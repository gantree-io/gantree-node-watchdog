"""Various misc. utilities."""
import requests

from .conditions import is_exception


class Expected200Error(Exception):
    """Error thrown when expect200 doesn't get a 200."""

    def __init__(self, res, *args, **kwargs):
        """See class docstring."""
        super().__init__(*args, **kwargs)
        self.res = res


class printStatus:
    def __init__(
        self,
        action: str,
        on_success: str = "OK",
        on_fail: str = "FAIL",
        suffix: str = "",
        fail_conditions=[],
    ):
        self.action = action
        self.on_success = on_success
        self.on_fail = on_fail
        self.suffix = suffix
        self.fail_conditions = [is_exception, *fail_conditions]

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

            print(self.on_success + self.suffix)
            return res

        return wrapper_printStatus


def expect200(func):
    """Return runtime error if response status code isn't 200."""

    def wrapper_expect200(*args, **kwargs):
        res = func(*args, **kwargs)
        if not isinstance(res, requests.Response):
            return TypeError(
                f"Response instance not returned from decorated function, instead got {type(res)}"
            )
        if res.ok:
            return res
        else:
            return Expected200Error(
                res,
                f"Expected 200, got {res.status_code}: {res.reason}"
                + "\nContent: {res.content.decode('utf-8')}",
            )

    return wrapper_expect200
