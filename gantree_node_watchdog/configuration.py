"""Management of configuration."""

import os
import json
from typing import Dict, Union


class Configuration:
    """Stores configuration options sourced from various origins."""

    def __init__(self, config_file: str = None, censor_values: bool = True) -> None:
        """See class docstring."""
        self.proxy_hostname = None
        self.metrics_hostname = None
        self.api_key = None
        self.project_id = None
        self.ip_address = None
        self.node_id = None
        self.node_secret = None
        self._keys = [key for key in dir(self) if key[:1] != "_"]
        self._key_origins: Dict[str, Union[None, str]] = {
            key: None for key in self._keys
        }
        if not isinstance(censor_values, bool):
            raise TypeError("censor_values must be bool")
        self._censor_values = censor_values

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

    def __repr__(self):
        """Represent the configuration as a table of options and origins."""
        string = ""
        longest_key = 0
        longest_origin = 0
        longest_value = 0

        for key in self._key_origins:

            len_key = len(key)
            if len_key > longest_key:
                longest_key = len_key

            origin = self._key_origins[key]
            if origin is not None:
                len_origin = len(origin)
                if len_origin > longest_origin:
                    longest_origin = len_origin

            value = getattr(self, key)
            if value is not None:
                len_value = len(value)
                if len_value > longest_value:
                    longest_value = len_value

        string += f"| {'OPTION':<{longest_key}} | {'ORIGIN':<{longest_origin}} | {'VALUE':<{longest_value}} |\n"
        string += f"| {'-' * longest_key} | {'-' * longest_origin} | {'-' * longest_value} |\n"
        for key in self._key_origins:
            origin = self._key_origins[key]
            value = getattr(self, key)
            if origin is not None:
                if self._censor_values:
                    string += f"| {key:<{longest_key}} | {origin:<{longest_origin}} | {value[:2] + '#' * (len(value)-4) + value[-2:]:<{longest_value}} |\n"
                else:
                    string += f"| {key:<{longest_key}} | {origin:<{longest_origin}} | {value:<{longest_value}} |\n"

        return string
