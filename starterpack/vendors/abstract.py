import subprocess
from threading import Thread


class Launcher(object):
    """Abstract class that must be overridden by vendor launchers.
    Those should handle the full process of starting and exiting properly the application."""

    def __init__(self):
        super(Launcher, self).__init__()
        self._running_thread: Thread = None

    def execute(self):
        cmd = self._cmd_to_exec()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        # Make sure to wait the end of process before destroying this Launcher.
        self._running_thread = Thread(target=lambda p: p.wait(), args=(process,))
        self._running_thread.start()

    def _cmd_to_exec(self):
        raise NotImplementedError()
