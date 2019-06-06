#!/bin/env python
from __future__ import annotations
import sys
import os

# Append the higher-level directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from w40k.battlescribe.models.utils import load_models_from_schema

ms = load_models_from_schema(sys.argv[1])
for m in ms:
    print(m)



