#!/bin/env python
import sys
import os
import pprint 

pp = pprint.PrettyPrinter(indent=2)

# Append the higher-level directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from w40k.battlescribe.importer import BattlescribeCatFile

if len(sys.argv) != 2:
    print("usage: python bin/import_battlescribe_file.py <battlescribe-filename>")
    sys.exit(-1)

with BattlescribeCatFile(sys.argv[1]) as bcf:
    publications = bcf.publications
    profile_types = bcf.profile_types
    category_entries = bcf.category_entries
    entry_links = bcf.entry_links
    rules = bcf.rules
    info_links = bcf.info_links
    shared_selection_entries = bcf.shared_selection_entries

if True:
    pp.pprint(publications)
    pp.pprint(profile_types)
    pp.pprint(category_entries)
    pp.pprint(entry_links)
    pp.pprint(rules)
    pp.pprint(info_links)
    pp.pprint(shared_selection_entries)