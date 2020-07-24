"""Management of configuration."""

import os
import json
from pathlib import Path
from typing import Dict, Union, Callable

import colorama

from ..conditions import is_false, is_client_id_valid
from ..utils import printStatus, get_public_ip_addr, read_json
from . import meta

HAS_REG_DETAILS_MESSAGE = (
    colorama.Fore.LIGHTBLUE_EX
    + "Checking registration details... "
    + colorama.Style.RESET_ALL
)
VALIDATION_MESSAGE = (
    colorama.Fore.LIGHTBLUE_EX
    + "Validating configuration... "
    + colorama.Style.RESET_ALL
)


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

        # TODO: move into options meta
        self._defaults = {
            "proxy_hostname": "https://prometheus.gantree.io",
            "metrics_hostname": "http://127.0.0.1:9615",
            "ip_address": get_public_ip_addr,
        }
        # TODO: move into options meta
        self._required_options = ["api_key", "project_id", "client_id", "ip_address"]
        # TODO: move into options meta
        self._checks = {"client_id": [is_client_id_valid]}

        self._keys = [key for key in dir(self) if key[:1] != "_"]
        self._key_origins: Dict[str, Union[None, str]] = {
            key: None for key in self._keys
        }

        self._config_file = config_file

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
                    json.dump({}, f, indent=4)
            with open(config_file, "r") as f:
                data = json.load(f)
                for key in self._keys:
                    if getattr(self, key) is None:
                        val = data.get(key)
                        if val is not None:
                            setattr(self, key, val)
                            self._key_origins[key] = "Configuration File"

        """Load default values."""
        default_executions_ran = False
        for dk in self._defaults:
            if getattr(self, dk) is None:
                dv: Union[str, Callable] = self._defaults[dk]
                if isinstance(dv, str):
                    setattr(self, dk, dv)
                    self._key_origins[dk] = "Defaults"
                else:
                    try:
                        # print(f"Getting '{dk}' from {dv.__name__}()...")
                        # default_executions_ran = True
                        setattr(self, dk, dv())
                        self._key_origins[dk] = "Defaults (Executed)"
                    except Exception as e:
                        raise RuntimeError(f"Failed to execute callable default: {e}")
        if default_executions_ran:
            print()  # newline for neatness

        """Prompt for missing values."""
        prompt_help_displayed = False
        for ro in self._required_options:
            if getattr(self, ro) is None:

                if not prompt_help_displayed:
                    print(
                        "⮞ One or more required options couldn't be"
                        + " found in your configuration file or environment variables."
                        + "\n⮞ You'll be prompted for any values we need right now."
                        + "\n⮞ Any information you enter will be stored in your configuration"
                        + f" file ('{self._config_file}') and will be loaded when the"
                        + " program is next executed."
                        + "\n"
                    )
                    prompt_help_displayed = True

                ro_input = input(
                    colorama.Fore.LIGHTBLUE_EX
                    + f"{meta.get_desc(ro)}: "
                    + colorama.Style.RESET_ALL
                )

                self._write_option_to_config(ro, ro_input)

                self._key_origins[ro] = "User Input"

        if prompt_help_displayed:
            print()  # newline for neatness

        # TODO: give users a change to update invalid options with prompt, also say the options origin (e.g. config)
        valid = self._validate()
        if isinstance(valid, Exception):
            print(valid)
            exit()
        elif valid is False:
            print("WIP: config failed to validate, no error supplied.")
        print()  # newline for neatness

    @printStatus(VALIDATION_MESSAGE)
    def _validate(self):
        invalid_values = []
        for ck in self._checks:
            if getattr(self, ck) is not None:
                for check in self._checks[ck]:
                    result = check(getattr(self, ck))

                    if isinstance(result, tuple):
                        result, result_msg = result

                    if isinstance(result, bool):
                        if not result:
                            return ValueError(
                                f"{ck} failed to validate"
                                + (
                                    f": {result_msg}"
                                    if result_msg
                                    else ": please check documentation for valid values"
                                )
                            )
                            # TODO: collect all failed checks and print at once instead of one at a time
                            # invalid_values.append({ck: result_msg})

                    else:
                        raise RuntimeError(
                            "A config check did not return a boolean or valid tuple"
                        )

        return True if len(invalid_values) == 0 else False

        # for i in range(len(invalid_values)):
        #     failed_checks = invalid_values[i]
        #     for invalid_value in failed_checks:
        #         print(invalid_value)
        #     # for key in failed_checks[failed]:
        #     #     print(f"{key} invalid - {failed_checks[failed]}")
        # exit()

    def _write_option_to_config(self, option, value, apply_now: bool = True):
        if self._config_file is not None:

            with open(self._config_file, "r") as f:  # read current config
                data = json.load(f)

            data[option] = value  # add user inputted key

            with open(self._config_file, "w") as f:  # write modified config
                json.dump(data, f, indent=4)

        if apply_now:
            setattr(self, option, value)  # apply to attribute

    def _save_registration_details(self, node_id, node_secret):
        self._write_option_to_config("node_id", node_id)
        self._write_option_to_config("node_secret", node_secret)

    @printStatus(HAS_REG_DETAILS_MESSAGE, fail_conditions=[is_false])
    def _has_registration_details(self):
        if self.node_id and self.node_secret:
            return True
        else:
            return False

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
                    censored_value = (
                        value[:2] + "#" * (len(value) - 4) + value[-2:]
                        if len(value) >= 4
                        else value
                    )
                    string += (
                        f"| {key:<{longest_option}} |"
                        + f" {origin:<{longest_origin}} |"
                        + f" {censored_value:<{longest_value}} |\n"
                    )
                else:
                    string += f"| {key:<{longest_option}} | {origin:<{longest_origin}} | {value:<{longest_value}} |\n"

        return string
