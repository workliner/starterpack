import importlib
from typing import List, Dict

import starterpack
import starterpack.vendors.abstract


class StarterPack(object):
    """Main class handling all the vendor launchers (provided as plugins)."""

    def __init__(self):
        super(StarterPack, self).__init__()

        self._vendor_launchers = {}
        self._load_vendor_launchers()

    def launch(self, name: str, **kwargs) -> None:
        """Execute a vendor launcher.

        Args:
            name: name of the vendor.
            **kwargs: optional arguments the vendor launcher may use.
        """
        launcher_cls = self._vendor_launchers.get(name, None)
        if not launcher_cls:
            raise AttributeError(f"The launcher for {name} is not loaded.")

        launcher = launcher_cls(**kwargs)
        launcher.execute()

    def get_vendor_launchers(self, only_name: bool = False) -> List[str] or Dict:
        return self._vendor_launchers if not only_name else list(self._vendor_launchers.keys())

    def _load_vendor_launchers(self) -> None:
        if self._vendor_launchers:
            # Not empty so already loaded.
            return

        for prefix, vendor in starterpack.find_vendor_pkgs():
            vendor_core_pkg = importlib.import_module(f".{vendor}.core", prefix)

            for func in ("can_be_registered", "register_launcher"):
                if not hasattr(vendor_core_pkg, func) or not callable(getattr(vendor_core_pkg, func)):
                    raise RuntimeError(f"The package {vendor_core_pkg} does not provide the function {func}.")

            if not vendor_core_pkg.can_be_registered():
                continue

            launcher_cls = vendor_core_pkg.register_launcher()
            if not issubclass(launcher_cls, starterpack.vendors.abstract.Launcher):
                raise RuntimeError(f"The loaded class {launcher_cls} does not inherit the abstract Launcher class.")

            self._vendor_launchers[vendor] = launcher_cls
