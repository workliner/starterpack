import sys
import argparse
import importlib

import starterpack


def execute(args):
    desc = (
        "Use one of the following keywords to launch the DCC you want. "
        "To get more help, add '-h' or '--help' after the software name you want to start. Example: 'afterfx -h'."
    )

    main_parser = argparse.ArgumentParser(description=desc)
    vendor_parsers_parent = main_parser.add_subparsers()
    vendor_cli_modules = _load_vendor_cli_modules(vendor_parsers_parent)

    # Important to load vendor modules before to populate dynamically the help.
    if not args:
        main_parser.print_help()
        return

    vendor_name = args[0]
    vendor_cli_module = vendor_cli_modules.get(vendor_name, None)
    if not vendor_cli_module:
        raise RuntimeError(f"The CLI for {vendor_name} is not loaded.")

    vendor_args = main_parser.parse_args(args)
    vendor_cli_module.execute(vendor_args)


def _load_vendor_cli_modules(parsers_parent):
    vendor_cli_modules = {}
    for prefix, vendor in starterpack.find_vendor_pkgs():
        vendor_cli_module = importlib.import_module(f".{vendor}.cli", prefix)

        for func in ("can_be_registered", "register_cli", "execute"):
            if not hasattr(vendor_cli_module, func) or not callable(getattr(vendor_cli_module, func)):
                raise RuntimeError(f"The module {vendor_cli_module} does not provide the function {func}.")

        if not vendor_cli_module.can_be_registered():
            continue

        vendor_parser = parsers_parent.add_parser(name=vendor)
        vendor_cli_module.register_cli(vendor_parser)
        vendor_cli_modules[vendor] = vendor_cli_module

    return vendor_cli_modules


if __name__ == "__main__":
    execute(sys.argv[1:])
