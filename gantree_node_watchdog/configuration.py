"""Management of configuration."""

import os
import json
from pathlib import Path
from typing import Dict, Union


class Configuration:
    """Stores configuration options sourced from various origins."""

    def __init__(self, config_file: str = None, censor_values: bool = True) -> None:
        """See class docstring."""
        self.proxy_hostname = None
        self.metrics_hostname = None
        self.api_key = None
        self.project_id = None
        self.client_id = None
        self.ip_address = None
        self.node_id = None
        self.node_secret = None

        self._defaults = {
            "proxy_hostname": "https://api.gantree.io",
            "metrics_hostname": "http://127.0.0.1:9615",
        }
        self._required_options = ["api_key", "project_id", "client_id", "ip_address"]

        self._keys = [key for key in dir(self) if key[:1] != "_"]
        self._key_origins: Dict[str, Union[None, str]] = {
            key: None for key in self._keys
        }

        if not isinstance(censor_values, bool):
            raise TypeError("censor_values must be bool")
        self._censor_values = censor_values

        """Load any values from environment variables matching an attribute."""
        for key in self._keys:
            if getattr(self, key) is None:
                env_var = "GANTREE_NODE_WATCHDOG_" + key.upper()
                val = os.getenv(env_var)
                if val is not None:
                    setattr(self, key, val)
                    self._key_origins[key] = "Environment Variable"

        """Load any values in the configuration file matching an attribute."""
        if config_file is not None:
            if not Path(config_file).is_file():
                with open(config_file, "w") as f:
                    json.dump({}, f)
            with open(config_file, "r") as f:
                data = json.load(f)
                for key in self._keys:
                    if getattr(self, key) is None:
                        val = data.get(key)
                        if val is not None:
                            setattr(self, key, val)
                            self._key_origins[key] = "Configuration File"

        """Load default values."""
        for dk in self._defaults:
            if getattr(self, dk) is None:
                setattr(self, dk, self._defaults[dk])
                self._key_origins[dk] = "Defaults"

        """Prompt for missing values."""
        if self.proxy_hostname is None:
            # write to config
            # apply to attribute
            self.proxy_hostname = input("Proxy hostname: ")

    def __repr__(self):
        """Represent the configuration as a table of options and origins."""
        string = ""
        option_header = "OPTION"
        origin_header = "ORIGIN"
        value_header = "VALUE"

        longest_option = len(option_header)
        longest_origin = len(origin_header)
        longest_value = len(value_header)

        for key in self._key_origins:

            len_key = len(key)
            if len_key > longest_option:
                longest_option = len_key

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

        # TODO: cut off table if it exceeds term columns (or alternative)
        string += f"| {option_header:<{longest_option}} | {origin_header:<{longest_origin}} | {value_header:<{longest_value}} |\n"
        string += f"| {'-' * longest_option} | {'-' * longest_origin} | {'-' * longest_value} |\n"
        for key in self._key_origins:
            origin = self._key_origins[key]
            origin = "?" if origin is None else origin
            value = getattr(self, key)
            value = "None" if value is None else value
            if origin is not None:
                if self._censor_values:
                    string += f"| {key:<{longest_option}} | {origin:<{longest_origin}} | {value[:2] + '#' * (len(value)-4) + value[-2:]:<{longest_value}} |\n"
                else:
                    string += f"| {key:<{longest_option}} | {origin:<{longest_origin}} | {value:<{longest_value}} |\n"

        return string
