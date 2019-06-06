from __future__ import annotations
from typing import List
from dataclasses import dataclass

from w40k.battlescribe.importer import BattlescribeCatFile

@dataclass
class Profile:
    m: int
    ws: int
    bs: int
    s: int
    t: int
    w: int
    a: int
    ld: int
    sv: int
    max: int
    has_max: bool

    def __repr__(self):
        format_str = " ".join(list(map(lambda x: "{" + str(x) + ": >3}", range(10))))
        s = format_str.format("M", "WS", "BS", "S", "T", "W", "A", "Ld", "Wv", "Max") + "\n"
        m_str = str(self.m) + '"'
        ws_str = str(self.ws) + "+"
        bs_str = str(self.ws) + "+"
        sv_str = str(self.sv) + "+"

        if self.has_max:
            max_value = self.max
        else:
            max_value = "-"
        
        s += format_str.format(m_str, ws_str, bs_str, self.s, self.t, self.w, self.a, sv_str, self.ld, max_value)
        return s

@dataclass
class Model:
    unit: str
    name: str
    profiles: List[Profile]

    def __repr__(self):
        s = f"{self.unit}: {self.name}\n"
        for p in self.profiles:
            s += str(p)
        return s
