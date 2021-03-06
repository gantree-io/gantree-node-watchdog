"""Collection of functions which return a boolean based on the properties of an item.

In some cases, an exception may be returned instead.

All functions should be usable in an iterable context.
"""
import re


def is_exception(item):
    """Self-explanatory."""
    return True if isinstance(item, Exception) else False


def is_false(item):
    """Self-explanatory."""
    return True if item is False else False


def is_403(item):
    """Return True if the item has a status_code of 403 (forbidden/unauthorized).
    
    Return TypeError if item doesn't have a status_code.
    """
    if hasattr(item, "status_code"):
        return (True, "Forbidden") if item.status_code == 403 else False

    return TypeError("is_403 cannot check item with missing status_code attribute")


def is_409(item):
    """Return True if the item has a status_code of 409 (conflict).
    
    Return TypeError if item doesn't have a status_code.
    """
    if hasattr(item, "status_code"):
        return (True, "Conflict") if item.status_code == 409 else False

    return TypeError("is_409 cannot check item with missing status_code attribute")


def dash_not_ready(item):
    """Return True if the item doesn't contains a telemDashboard status other than ready.

    Return ValueError if item doesn't return the expected data shape.

    Return RuntimeError if item's .json() method raises an error.
    """
    if not hasattr(item, "json"):
        return ValueError("dash_not_ready cannot check item without a json method")

    item_json = None
    try:
        item_json = item.json()
    except Exception as e:
        return RuntimeError(
            f"dash_not_ready encountered an error while running the item's .json() method:\n{e.__repr__()}"
        )

    if not ("status" in item_json):
        return ValueError(
            "dash_not_ready cannot check item without a status key in content"
        )

    if not ("telemDashboard" in item_json["status"]):
        return ValueError(
            "dash_not_ready cannot check item without status.telemDashboard key"
        )

    if item_json["status"]["telemDashboard"] == "READY":
        return False
    else:
        return (True, f"Status = {item_json['status']['telemDashboard']}")


def is_client_id_valid(client_id):
    exp = r"^[a-z\-0-9]{0,64}$"
    m = re.match(exp, client_id)
    if m:
        return True
    else:
        return (False, f"client_id must match this regex: {exp}")
