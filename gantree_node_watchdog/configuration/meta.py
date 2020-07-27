"""Configuration metadata."""

from .. import internal_error_message

"""Information on option dict:

[description] - Description of the option, should be short.

[default] - Default value for an option.

[promptable] - Whether users should be prompted to fill in this option.
             - Holds no bearing as to if values can be overwritten by other methods.
"""
OPTIONS: dict = {
    "proxy_hostname": {
        "description": "PLACEHOLDER",
        "default": "PLACEHOLDER",
        "promptable": False,
    },
    "metrics_hostname": {
        "description": "PLACEHOLDER",
        "default": "PLACEHOLDER",
        "promptable": False,
    },
    "api_key": {
        "description": "API key from the Gantree web app",
        "default": None,
        "promptable": True,
    },
    "project_id": {
        "description": "Name of substrate network",
        "default": None,
        "promptable": True,
    },
    "client_id": {
        "description": "Name of this node",
        "default": None,
        "promptable": True,
    },
    "ip_address": {
        "description": "Public IP address for this node",
        "default": "PLACEHOLDER",
        "promptable": False,
    },
    "node_id": {
        "description": "Server ID for this node",
        "default": None,
        "promptable": False,
    },
    "node_secret": {"description": "PLACEHOLDER", "default": None, "promptable": False},
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
