from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass

from w40k.battlescribe.importer import BattlescribeCatFile
from w40k.battlescribe.models.model import Model, Profile

def _int(val: str) -> Optional(int):
    try:
        return int(val)
    except:
        return None

def _clean_plus_characteristic(val: str) -> str:
    return val.replace("+", "")

def _clean_inch_characteristic(val: str) -> str:
    return val.replace('"', "")

def load_models_from_schema(fname: str) -> List[Model]:
    def characteristics_to_profile(cs):
        cs_m = {}
        for c in cs:
            cs_m[c["name"]] = c["value"]
        args = {}
        for arg in ["M", "WS", "BS", "S", "T", "W", "A", "Ld", "Sv", "Max"]:
            args[arg.lower()] = _int(_clean_inch_characteristic(_clean_plus_characteristic(cs_m[arg])))
        args["has_max"] = (args["max"] != None)
        print(args)
        return Profile(**args)

    models = []
    bs = BattlescribeCatFile(fname)
    for sse in bs.shared_selection_entries:
        if sse["type"] == "model":
            m = Model(unit=sse["name"], name=sse["name"], profiles=[])
            for p in sse["profiles"]:
                if p.get("type_name", None) == "Model":
                    cs = p.get("characteristics", [])
                    m.profiles.append(characteristics_to_profile(cs))

            models.append(m)

    return models
