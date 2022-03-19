import os
from typing import List, Dict
from pathlib import Path
import logging
import json
import shlex

AFTERFX_BIN = "WL_SP_AFTERFX_BIN"
JS_SCRIPT_OBJECT_NAME = "WL_SP_DATA"


class _CommandBuilder(object):
    """Used to build an AfterFX command with some potential arguments."""

    def __init__(
            self, bin_path: str = None, no_gui: bool = False, script_path: str = None, script_args: Dict = None
    ) -> None:
        super(_CommandBuilder, self).__init__()

        # Checking.
        bin_path = bin_path or os.getenv(AFTERFX_BIN, None)
        if not bin_path or not Path(bin_path).exists():
            raise FileExistsError(
                "You should provide a valid path for the AfterFX binary: "
                f"either through argument or through the env var {AFTERFX_BIN}."
            )

        if no_gui and not script_path:
            raise AttributeError("You cannot run AfterFX in no-gui mode without specifying a script to execute.")
        if script_args and not script_path:
            raise AttributeError("You cannot provide script arguments without specifying a script to execute.")

        if script_path is not None:
            path = Path(script_path)
            if not path.exists():
                raise FileExistsError("You should provide a valid path for the AfterFX script to execute.")
            if path.suffix not in (".js", ".jsx"):
                raise ValueError("The AfterFX script provided should have the '.js' or '.jsx' extension.")

        # Storing.
        self._bin_path = bin_path
        self._no_gui = no_gui
        self._script_path = script_path
        self._script_args = script_args

        logging.info(self._info())

    def _info(self):
        msg_info = f"CommandBuilder for AfterFX ({self._bin_path})."
        if self._no_gui:
            msg_info += " The instance will run in no-gui mode."
        if self._script_path:
            msg_info += f" The following script will be executed at startup: {self._script_path}."
        if self._script_args:
            msg_info += f" The arguments for the script will be the following ones: {self._script_args}."

        return msg_info

    def build(self) -> List[str]:
        """Build the AfterFX command based on specified flags and script arguments.

        Returns:
            List[str]: the full command to process.
        """
        logging.debug(f"Building command for {self}.")

        # Add the AfterFX binary in the first place.
        cmd = [self._bin_path]

        # Set the batch/UI mode.
        if self._no_gui:
            cmd.append("-noui")

        # Workaround to make AfterFX running the specified
        # script with the good arguments.
        # We send to the command an inline script which will
        # make sure to execute the real script.
        if self._script_path:
            cmd.append("-s")

            inline_script = []
            if self._script_args:
                inline_script.extend(
                    [
                        f"#include {Path(__file__).parent / 'jsx_utils' / 'json_reader.js'};",
                        f"var {JS_SCRIPT_OBJECT_NAME} = readJsonString({shlex.quote(json.dumps(self._script_args))});",
                    ]
                )

            script_path = self._script_path.replace("\\", "/")
            inline_script.extend(
                [
                    f"app.exitAfterLaunchAndEval={str(self._no_gui).lower()};",
                    f"$.evalFile('{script_path}');",  # shlex.quote does not work here if there is no spaces to quote.
                ]
            )

            cmd.append("".join(inline_script))

        logging.debug(f"The generated command is: {cmd}")

        return cmd
