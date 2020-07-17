"""Collection of functions which return a boolean based on the properties of an item.

In some cases, an exception may be returned instead.

All functions should be usable in an iterable context.
"""


def is_exception(item):
    """Self-explanatory."""
    return True if isinstance(item, Exception) else False


def is_false(item):
    """Self-explanatory."""
    return True if item is False else False


def is_409(item):
    """Return True if the item has a status_code of 409.
    
    Return TypeError if item doesn't have a status_code.
    """
    if hasattr(item, "status_code"):
        return True if item.status_code == 409 else False
    return TypeError("is_409 cannot check item with missing status_code attribute")
