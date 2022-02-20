def can_be_registered():
    import sys

    if not sys.platform == "win32":
        return False
    return True
