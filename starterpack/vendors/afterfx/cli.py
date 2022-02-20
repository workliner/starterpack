def can_be_registered():
    import starterpack.vendors.afterfx

    return starterpack.vendors.afterfx.can_be_registered()


def register_cli(parser_to_configure):
    parser_to_configure.add_argument("--bin-path", dest="bin_path", type=str, help="Path to the application binary.")


def execute(args):
    from starterpack.vendors.afterfx.core.launcher import Launcher

    launcher = Launcher(bin_path=args.bin_path)
    launcher.execute()
