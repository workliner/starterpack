import os
from typing import List
from pathlib import Path
import logging

AFTERFX_BIN = "WL_SP_AFTERFX_BIN"


class _CommandBuilder(object):
    """Used to build an AfterFX command with some potential arguments."""

    def __init__(self, bin_path: str = None, no_gui: bool = False, script_path: str = None) -> None:
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

        logging.info(self._info())

    def _info(self):
        msg_info = f"CommandBuilder for AfterFX ({self._bin_path})."
        if self._no_gui:
            msg_info += " The instance will run in no-gui mode."
        if self._script_path:
            msg_info += f" The following script will be executed at startup: {self._script_path}."

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
        # script with the good arguments (for later implementation).
        # We send to the command an inline script which will
        # make sure to execute the real script.
        if self._script_path:
            script_path = self._script_path.replace("\\", "/")
            cmd.append("-s")
            inline_script = [
                f"app.exitAfterLaunchAndEval={str(self._no_gui).lower()};",
                f"$.evalFile('{script_path}');",
            ]

            cmd.append("".join(inline_script))

        return cmd
