class Launcher(object):
    """Abstract class that must be overridden by vendor launchers.
    Those should handle the full process of starting and exiting properly the application."""

    def execute(self):
        raise NotImplementedError()
