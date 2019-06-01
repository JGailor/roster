import json
from w40k import Weapon, Model

def weapon_wound_roll_target(weapon: Weapon, target: Model) -> float:
    if weapon.s > (2 * target.t):
        return 2
    elif weapon.s > target.t:
        return 3
    elif weapon.s == target.t:
        return 4
    elif weapon.s < target.t:
        return 5
