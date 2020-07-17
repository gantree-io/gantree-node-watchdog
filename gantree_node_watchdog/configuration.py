import os
import json


class Configuration:
    def __init__(self, config_file=None):
        self.proxy_hostname = None
        self.metrics_hostname = None
        self.api_key = None
        self.project_id = None
        self.ip_address = None
        self.node_id = None
        self.node_secret = None
        self._keys = [key for key in dir(self) if key[:1] != "_"]
        self._key_origins = {key: None for key in self._keys}

        """Load any values from environment variables matching an attribute"""
        for key in self._keys:
            if getattr(self, key) is None:
                env_var = "GANTREE_NODE_WATCHDOG_" + key.upper()
                val = os.getenv(env_var)
                if val is not None:
                    setattr(self, key, val)
                    self._key_origins[key] = "Environment Variable"

        """Load any values in the configuration file matching an attribute"""
        if config_file is not None:
            with open(config_file, "r") as f:
                data = json.load(f)
                for key in self._keys:
                    if getattr(self, key) is None:
                        val = data.get(key)
                        if val is not None:
                            setattr(self, key, val)
                            self._key_origins[key] = "Configuration File"


        os.getenv("GANTREE_NODE_WATCHDOG_PROXY_HOSTNAME")


def get_env_vars():
    """Fetch required environment variables."""
    return {
        # "proxy_hostname": ,
        "metrics_hostname": os.getenv("GANTREE_NODE_WATCHDOG_METRICS_HOSTNAME"),
        "api_key": os.getenv("GANTREE_NODE_WATCHDOG_API_KEY"),
        "project_id": os.getenv("GANTREE_NODE_WATCHDOG_PROJECT_ID"),
        "ip_address": os.getenv("GANTREE_NODE_WATCHDOG_IP_ADDRESS"),
        "node_id": os.getenv("GANTREE_NODE_WATCHDOG_NODE_ID"),
        "node_secret": os.getenv("GANTREE_NODE_WATCHDOG_NODE_SECRET"),
    }
