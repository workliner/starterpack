def can_be_registered():
    import starterpack.vendors.afterfx

    return starterpack.vendors.afterfx.can_be_registered()


def register_launcher():
    import starterpack.vendors.afterfx.core.launcher

    return starterpack.vendors.afterfx.core.launcher.Launcher
