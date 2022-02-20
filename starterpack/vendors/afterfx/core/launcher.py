import os
from pathlib import Path
import logging
import subprocess
from threading import Thread

import psutil

import starterpack.vendors.abstract

WL_SP_AFTERFX_BIN = "WL_SP_AFTERFX_BIN"


class Launcher(starterpack.vendors.abstract.Launcher):
    """AfterFX launcher.

    Args:
        bin_path: (optional) path to the AfterFX binary.
    """

    def __init__(self, bin_path: str = None) -> None:
        super(Launcher, self).__init__()

        # Checking.
        bin_path = bin_path or os.getenv(WL_SP_AFTERFX_BIN, None)
        if not bin_path or not Path(bin_path).exists():
            raise FileExistsError(
                "You should provide a valid path for the AfterFX binary: "
                f"either through argument or through the env var {WL_SP_AFTERFX_BIN}."
            )

        # Storing.
        self._bin_path: str = bin_path

        # Useful variables.
        self._running_thread: Thread = None

        logging.info(f"Creating a Launcher for AfterFX ({bin_path}).")

    def execute(self) -> None:
        self._execute_ui()

    def _execute_ui(self) -> None:
        if "AfterFX.exe" in (p.name() for p in psutil.process_iter()):
            logging.warning("There is already a running AfterFX UI.")
        else:
            self._open_afterfx_ui()

    def _open_afterfx_ui(self) -> None:
        logging.debug("Opening AfterFX UI.")

        cmd = [self._bin_path]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        # Make sure to wait the AfterFX close before destroying this Launcher.
        self._running_thread = Thread(target=lambda p: p.wait(), args=(process,))
        self._running_thread.start()
