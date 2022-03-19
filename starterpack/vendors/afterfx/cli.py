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


def execute(args):
    from starterpack.vendors.afterfx.core.launcher import Launcher

    launcher = Launcher(bin_path=args.bin_path, no_gui=args.no_gui, script_path=args.script_path)
    launcher.execute()
