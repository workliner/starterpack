import os

import starterpack.vendors.abstract
from starterpack.vendors.afterfx.core.command_builder import _CommandBuilder


class Launcher(starterpack.vendors.abstract.Launcher):
    """AfterFX launcher.

    Args:
        bin_path: (optional) path to the AfterFX binary.
        no_gui: (optional) run the application in batch mode. Works only when 'script_path' is set.
        script_path: (optional) path to an AfterFX script to execute at startup.
    """

    def __init__(self, bin_path: str = None, no_gui: bool = False, script_path: str = None) -> None:
        super(Launcher, self).__init__()

        self._cmd_builder = _CommandBuilder(bin_path=bin_path, no_gui=no_gui, script_path=script_path)

    def _cmd_to_exec(self):
        return self._cmd_builder.build()
