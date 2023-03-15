#!/usr/bin/env python3

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
