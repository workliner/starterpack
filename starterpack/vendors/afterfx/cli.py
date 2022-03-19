import ast


def can_be_registered():
    import starterpack.vendors.afterfx

    return starterpack.vendors.afterfx.can_be_registered()


def register_cli(parser_to_configure):
    parser_to_configure.add_argument("--bin-path", dest="bin_path", type=str, help="Path to the application binary.")
    parser_to_configure.add_argument(
        "--no-gui",
        dest="no_gui",
        action="store_true",
        help="Run the application in batch mode (without GUI).",
    )
    parser_to_configure.add_argument(
        "--script-path", dest="script_path", type=str, help="Path to an AfterFX script to execute at startup."
    )
    parser_to_configure.add_argument(
        "--script-args",
        dest="script_args",
        type=str,
        nargs="*",
        help="Arguments for the script to execute. Syntax: key value key value...",
    )


def execute(args):
    from starterpack.vendors.afterfx.core.launcher import Launcher

    launcher = Launcher(
        bin_path=args.bin_path,
        no_gui=args.no_gui,
        script_path=args.script_path,
        script_args=_format_script_args(args.script_args),
    )
    launcher.execute()


def _format_script_args(script_args_list):
    if not script_args_list:
        return None

    if not len(script_args_list) % 2 == 0:
        raise ValueError(
            "The '--script-args' flag should be followed by an even number of elements. "
            "Indeed, it is represented like: key value key value key value..."
        )

    formatted_script_args = {}
    for i in range(int(len(script_args_list) / 2)):
        key = script_args_list[i * 2]
        value = __auto_convert(script_args_list[i * 2 + 1])
        formatted_script_args[key] = value

    return formatted_script_args


# https://stackoverflow.com/a/7019325
def __auto_convert(string: str):
    """Auto convert a string to its real type representation.

    Args:
        string: string to convert.
    """
    try:
        return ast.literal_eval(string)
    except ValueError:
        return string  # Probably a real string.
    except SyntaxError:
        return string  # Probably a real string.
