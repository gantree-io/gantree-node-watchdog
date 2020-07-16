import os


def get_env_vars():
    """Fetch required environment variables."""
    return {
        "hostname": os.getenv("GANTREE_NODE_WATCHDOG_HOSTNAME"),
        "api_key": os.getenv("GANTREE_NODE_WATCHDOG_API_KEY"),
        "project_id": os.getenv("GANTREE_NODE_WATCHDOG_PROJECT_ID"),
        "ip_address": os.getenv("GANTREE_NODE_WATCHDOG_IP_ADDRESS"),
        "node_id": os.getenv("GANTREE_NODE_WATCHDOG_NODE_ID"),
        "node_secret": os.getenv("GANTREE_NODE_WATCHDOG_NODE_SECRET"),
    }
