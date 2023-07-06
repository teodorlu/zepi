#!/usr/bin/env python3

# Develop Zepi with rapid feedback
#
# Quickstart
# ==========
#
# I prefer to have the following when I work with zepi:
#
# - Proper readline editing (Ctrl+R, cursor movement, etc)
# - A REPL
# - The ability to reload the language without restarting the REPL
#
# To get that workflow, please run:
#
#     rlwrap python launch.py repl
#
# Where rlwrap priovides GNU readline-style command editing. rlwrap can be
# downloaded from https://github.com/hanslub42/rlwrap.
#
# References
# ==========
#
# Inspired by hotload:
#
#   https://github.com/teodorlu/hotload

import importlib
import zepi

def zepi_reload(_incantation):
    importlib.reload(zepi)

def pyeval(incantation):
    incantation = incantation.strip()[len("!pyeval"):]
    try:
        print(eval(incantation))
    except:
        import traceback
        traceback.print_exc()

def magic_kaboom(_incantation):
    raise zepi.MagicFailed("💥")

def spells(_incantation):
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
