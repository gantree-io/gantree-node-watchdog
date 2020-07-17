"""Various misc. utilities."""
import requests

from .conditions import is_exception


class Expected200Error(Exception):
    """Error thrown when expect200 doesn't get a 200."""

    def __init__(self, res, *args, **kwargs):
        """See class docstring."""
        super().__init__(*args, **kwargs)
        self.res = res

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
