def expect200(res):
    """Return runtime error if response status code isn't 200."""
    if res.status_code == 200:
        return res
    else:
        return RuntimeError(f"Failed to register node: {res.reason}")
