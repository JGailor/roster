#!/bin/env python
import sys
import os
import pprint 
import xml.sax
import json

pp = pprint.PrettyPrinter(indent=2)

# Append the higher-level directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from w40k.battlescribe.schema import BattlescribeCatSchema

if len(sys.argv) != 2:
    print("usage: python bin/dump_battlescribe_schema.py <battlescribe-filename>")
    sys.exit(-1)

schema = BattlescribeCatSchema.parse(sys.argv[1])

print(json.dumps(schema.schema_tree))