def is_exception(item):
    return True if isinstance(item, Exception) else False


def is_false(item):
    return True if item is False else False


def is_409(item):
    if hasattr(item, "status_code"):
        return True if item.status_code == 409 else False
    return TypeError("is_409 cannot check item with missing status_code attribute")
