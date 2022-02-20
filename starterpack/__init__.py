def find_vendor_pkgs():
    import pkgutil
    import os

    vendor_dirname = "vendors"
    pkgs_location = os.path.join(__path__[0], vendor_dirname)
    pkgs_prefix = f"{__name__}.{vendor_dirname}"

    return [(pkgs_prefix, modname) for importer, modname, ispkg in pkgutil.iter_modules(path=[pkgs_location]) if ispkg]
