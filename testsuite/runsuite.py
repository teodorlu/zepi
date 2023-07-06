#!/usr/bin/env python3
#
# Usage:
#
#     ./runsuite.py JSONSUITE INTERPRETER
#
# To run with the privovided JSON suite and the provided interpreter:
#
#     ./runsuite.py suite.json "python ../zepi.py repl"

import json
import sys

def read_json_file(path):
    with open(path, "r") as f:
        jsondata = json.loads(f.read())
    return jsondata

def todo():
    suite = read_json_file(sys.argv[1])
