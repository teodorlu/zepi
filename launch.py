#!/usr/bin/env python3

# A launch script for Zepi that adds support for self reloading
#
# Inspired by hotload:
#
#   https://github.com/teodorlu/hotload

import importlib
import zepi

def zepi_reload(_invocation):
    importlib.reload(zepi)

def pyeval(invocation):
    invocation = invocation.strip()[len("!pyeval"):]
    try:
        print(eval(invocation))
    except:
        import traceback
        traceback.print_exc()

def magic_kaboom(invocation):
    raise zepi.MagicFailed("💥")

def spells(_invocation):
    for k in magic.keys():
        print(k)

magic = {
    "!zreload": zepi_reload,
    "!pyeval": pyeval,
    "!kaboom": magic_kaboom,
    "!spells": spells
}

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "repl":
        zepi.repl(magic)
