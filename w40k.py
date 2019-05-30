from dataclasses import dataclass
from __future__ import annotations
from typing import List
from math import floor
from w40k_utils import weapon_wound_roll_target
from enum import Enum

class DiceAverage(Enum):
    D3 = 2.0
    D6 = 3.5

@dataclass
class Ability:
    id: int
    name: str
    desc: str

@dataclass
class FactionKeyword:
    id: int
    name: str

@dataclass
class Keyword:
    id: int
    name: str

@dataclass
class WeaponType:
    id: int
    name: str

@dataclass
class WeaponAbility:
    id: int
    name: str
    desc: str
    reroll_hits_of_one: bool
    reroll_wounds_of_one: bool
    reroll_failed_hits: bool
    reroll_failed_wounds: bool

@dataclass
class Weapon:
    name: str

    range: int

    type: WeaponType

    # Ex: For a weapon with D3, the hit_value is 1 and the hit_die is 3
    hit_value: int
    hit_die: int 

    s: int
    ap: int
    d: int
    d_die: int 

    abilities: List[WeaponAbility] = []

    _reroll_hits_of_one: bool = None
    _reroll_wounds_of_one: bool = None

    _reroll_failed_hits: bool = None
    _reroll_failed_wounds: bool = None
    
    _autohit: bool = None

    # Melta Weapons
    half_range_roll_two_dice: bool

    # Plasma Supercharge
    kill_attacker_on_hit_roll_one: bool

    # Hit roll modifier
    hit_roll_modifier: int

    # Points
    points: int

    @property
    def reroll_hits_of_one(self) -> bool:
        if _reroll_hits_of_one is None:
            _reroll_hits_of_one = len(list(filter(lambda a: a.reroll_hits_of_one, self.abilities))) > 0
        return _reroll_hits_of_one
    
    @property
    def reroll_wounds_of_one(self) -> bool:
        if _reroll_wounds_of_one is None:
            _reroll_wounds_of_one = len(list(filter(lambda a: a.reroll_woudns_of_one, self.abilities))) > 0
        return _reroll_wounds_of_one

    @property
    def reroll_failed_hits(self) -> bool:
        if _reroll_failed_hits is None:
            _reroll_failed_hits = len(list(filter(lambda a: a.reroll_failed_hits, self.abilities))) > 0
        return _reroll_failed_hits

    @property
    def reroll_failed_wounds(self) -> bool:
        if _reroll_failed_wounds is None:
            _reroll_failed_wounds = len(list(filter(lambda a: a.reroll_failed_hits, self.abilities))) > 0
        return _reroll_failed_wounds

    # Calculates the average shots fired, taking into account weapons with random hits
    def avg_shots_fired(self):
        if self.hit_die == 3:
            return self.hit_value * DiceAverage.D3
        elif self.hit_die == 6:
            return self.hit_value * DiceAverage.D6 
        else:
            return self.hit_value

    def avg_d(self):
        if self.d_die == 6:
            return self.d * 3.5
        elif self.d_die == 3:
            return self.d * 2
        else:
            # No dice roll for damage, flat number
            return self.d


@dataclass
class Model:
    model_type: str

    m: int
    ws: int
    bs: int
    s: int
    t: int
    w: int
    a: int
    ld: int
    sv: int
    inv_sv: int

    weapons: List[Weapon] = []
    abilities: List[Ability] = []
    faction_keywords: List[FactionKeyword] = []
    keywords: List[Keyword] = []

    def ranged_weapons(self):
        return list(filter(lambda w: w.weapon_type != "Melee"))

    def best_save(self, weapon):
        if self.inv_sv:
            return max(self.sv + abs(weapon.ap), self.inv_sv)
        else:
            return self.sv + abs(weapon.ap)

    def shoot_against(self, target: Model):
        for weapon in self.ranged_weapons():
            avg_shots_connected = self.avg_shots_connected_for_weapon(weapon)
            avg_wounds = self.avg_wounds(avg_shots_connected, target, avg_shots_connected)

    def avg_shots_connected_for_weapon(self, weapon: Weapon) -> float:
        if weapon.autohit:
            return weapon.avg_shots_fired
        else:
            return weapon.avg_shots_fired * ((6 - self.bs - 1) / 6)

    def avg_wounds(self, shots_landed: float, target: Model, weapon: Weapon) -> float:
        wound_roll_target = weapon_wound_roll_target(weapon, target) 
        avg_wounds_landing = shots_landed * ((6 - (wound_roll_target - 1)) / 6) * ((6 - target.best_save(weapon) - 1) / 6)

        return avg_wounds_landing
    
    def avg_damage(self, wounds: float, weapon: Weapon) -> float:
        return wounds * weapon.avg_d()

@dataclass
class DisgustinglyResilient(Model):
    def avg_damage(self, wounds: float, weapon: Weapon) -> float:
        super().avg_damage(wounds, weapon) * self.disgustingly_resilient_modifier

    @property
    def disgustingly_resilient_modifier(self) -> float:
        return (4 / 6)    # (6 - (5 - 1)) / 6 
