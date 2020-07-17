"""Custom exceptions."""


class Expected200Error(Exception):
    """Error thrown when expect200 doesn't get a 200."""

    def __init__(self, res, *args, **kwargs):
        """See class docstring."""
        super().__init__(*args, **kwargs)
        self.res = res
