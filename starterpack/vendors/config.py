import logging
import os
from typing import Dict
from pathlib import Path

import yaml

GLOBAL_CONFIG_PATH = "WL_SP_CONFIG"


class _Config(object):
    def __init__(self, soft_name: str, soft_version: str = None):
        super(_Config, self).__init__()

        self._soft_name = soft_name
        self._soft_version = soft_version

        self._data = {}
        self._load()
        self._populate_environ()

    @property
    def env_vars(self) -> Dict:
        return self._data.get("env_vars", {})

    @property
    def current_soft(self) -> Dict:
        return self._data.get("current_soft", {})

    def _load(self) -> None:
        self._load_global_config()
        self._load_soft_config()

        logging.debug(f"After loading, config data is: {self._data}")

    @staticmethod
    def _read_config_file(filepath) -> Dict or None:
        if not filepath or not Path(filepath).exists():
            return None
        with open(filepath) as f:
            return yaml.load(f, yaml.CLoader)

    def _get_soft_config_path(self) -> str or None:
        return self._data.get("software_configs", {}).get(self._soft_name, None)

    def _load_global_config(self):
        global_data = self._read_config_file(os.getenv(GLOBAL_CONFIG_PATH, None))
        if not global_data:
            logging.warning(
                f"The global config is nonexistent or empty. Ensure the env var {GLOBAL_CONFIG_PATH} is set."
            )
            return

        self._data.update(global_data)

    def _load_soft_config(self):
        soft_data = self._read_config_file(self._get_soft_config_path())
        if not soft_data:
            logging.warning(
                f"The software config is nonexistent or empty. Ensure its path is set inside the global config."
            )
            return

        # Prepare data to keep.
        data_to_keep = {}

        # Ensure to keep current env_vars and to override them only if needed.
        global_env_vars = self._data.get("env_vars", {}).copy()
        soft_env_vars = soft_data.get("env_vars", {})
        global_env_vars.update(soft_env_vars)
        data_to_keep["env_vars"] = global_env_vars

        # Get only settings for the version we want to run.
        available_versions = soft_data.get("versions", {})
        if not self._soft_version:
            self._soft_version = sorted(available_versions.keys())[-1]  # latest by default.
        version_settings = available_versions.get(self._soft_version, {})
        data_to_keep["current_soft"] = version_settings

        self._data.update(data_to_keep)

    def _populate_environ(self):
        def recursive(dictionary):
            # Current level.
            env_vars: Dict = dictionary.get("env_vars", None)
            if env_vars:
                for var_name, var_value in env_vars.items():
                    os.environ[var_name] = var_value

            # Deeper level.
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    recursive(value)

        recursive(self._data)
