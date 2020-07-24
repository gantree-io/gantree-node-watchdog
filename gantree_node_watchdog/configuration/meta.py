"""Configuration metadata."""

from .. import internal_error_message


OPTIONS: dict = {
    "proxy_hostname": {"description": "PLACEHOLDER"},
    "metrics_hostname": {"description": "PLACEHOLDER"},
    "api_key": {"description": "PLACEHOLDER"},
    "project_id": {"description": "PLACEHOLDER"},
    "client_id": {"description": "PLACEHOLDER"},
    "ip_address": {"description": "PLACEHOLDER"},
    "node_id": {"description": "PLACEHOLDER"},
    "node_secret": {"description": "PLACEHOLDER"},
}


def get_desc(option_name):
    """Get an option's description.
    
    This function exists so descriptions are always fetched in the exact same way.
    """
    if option_name not in OPTIONS:
        raise Exception(
            f"Option '{option_name}' is missing metadata. " + internal_error_message
        )

    if "description" not in OPTIONS[option_name]:
        raise Exception(
            f"Option '{option_name}' is missing a description. "
            + internal_error_message
        )

    return OPTIONS[option_name]["description"]
