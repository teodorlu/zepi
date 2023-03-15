#!/usr/bin/env python3

# A launch script for Zepi that adds support for self reloading
#
# If you're interested in hotloading for a fast Python feedback loop, check out
# teodorlu/hotload:
#
#   https://github.com/teodorlu/hotload

import importlib
import zepi

def zepi_reload():
    importlib.reload(zepi)

magic={
    "!zreload": zepi_reload
}

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "repl":
        zepi.repl(magic)
