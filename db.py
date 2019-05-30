from __future__ import annotations
from typing import Dict
import json

from w40k import Model, DisgustinglyResilient, Weapon, WeaponType, WeaponAbility, Ability, FactionKeyword, Keyword

def load_db(file):
    with open(file, "r") as f:
        db = json.loads(f.read())

    abilities_db: Dict[int, Ability] = {}
    faction_keywords_db: Dict[int, FactionKeyword] = {}
    keywords_db: Dict[int, Keyword] = {}
    weapon_abilities_db: Dict[int, WeaponAbility] = {}
    weapon_type_db: Dict[int, WeaponType] = {}
    weapons_db: Dict[int, Weapon] = {}
    models_db: Dict[int, Model] = {}

    for ability in db["abilities"]:
        abilities_db[ability["id"]] = load_ability(ability)

    for faction_kw in db["faction_keywords"]:
        faction_keywords_db[faction_kw["id"]] = load_faction_keyword(faction_kw)

    for kw in db["keywords"]:
        keywords_db[kw["id"]] = load_keyword(kw)

    for weapon_ability in db["weapon_abilities"]:
        weapon_abilities_db[weapon_ability["id"]] = load_weapon_ability(weapon_ability)

    for weapon_type in db["weapon_types"]:
        weapon_type_db[weapon_type["id"]] = load_weapon_type(weapon_type)

    for weapon in db["weapons"]:
        weapons_db[weapon["id"]] = load_weapon(weapon, weapon_type_db, weapon_abilities_db)

    for model in db["models"]:
        models_db[model["id"]] = load_model(model, weapons_db, abilities_db, faction_keywords_db, keywords_db)

    return db

def load_ability(ab) -> Ability:
    return Ability(ab["id"], ab["name"], ab["desc"])

def load_faction_keyword(fkw) -> FactionKeyword:
    return FactionKeyword(fkw["id"], fkw["name"])

def load_keyword(kw) -> Keyword:
    return Keyword(kw["id"], kw["name"])

def load_weapon_ability(wa) -> WeaponAbility:
    a = WeaponAbility()
    a.id = wa["id"]
    a.name = wa["name"]
    a.desc = wa["desc"]
    a.reroll_failed_hits = wa["rr_failed_hits"] == True
    a.reroll_failed_wounds = wa["rr_failed_wounds"] == True
    a.reroll_hits_of_one = wa["rr_hits_one"] == True
    a.reroll_wounds_of_one = wa["rr_wounds_one"] == True

    return a

def load_weapon_type(wt) -> WeaponType:
    return WeaponType(wt["id"], wt["name"])

def load_weapon(weapon, weapon_type_db, weapon_abilities_db) -> Weapon:
    w = Weapon()
    w.name = weapon["name"]
    w.range = weapon["range"]
    if weapon["type"] in weapon_type_db.keys:
        w.type = weapon_type_db[weapon["type"]]
    else:
        raise Exception(f"Could not find weapon type id {weapon['type']} in the weapon types database")

    w.hit_value = weapon["hit_value"]
    w.hit_die = weapon["hit_die"]
    w.s = weapon["s"]
    w.ap = weapon["ap"]
    w.d = weapon["d"]
    w.d_die = weapon["d_die"]

    for ability in weapon["abilities"]:
        if ability in weapon_abilities_db.keys:
            w.abilities.append(weapon_abilities_db[ability])
        else:
            raise Exception(f"Could not find weapon ability id {ability} in the weapon abilities database")

    return w

def load_model(model, weapons_db, abilities_db, faction_keywords_db, keywords_db):
    stats = model["stats"]
    
    # Disgustingly Resilient
    if 2 in model["abilities"]:
        m = DisgustinglyResilient()
        
    m.model_type = model["designation"]
    m.m = stats["m"]
    m.ws = stats["ws"]
    m.bs = stats["bs"]
    m.s = stats["s"]
    m.t = stats["t"]
    m.w = stats["w"]
    m.a = stats["a"]
    m.ld = stats["ld"]
    m.sv = stats["sv"]
    m.inv_sv = stats["inv_sv"]

    for weapon in model["weapons"]:
        if not weapon in weapons_db.keys():
            raise Exception(f"Could not find weapon id {weapon} in the weapons database")
        model.weapons.append(weapons_db[weapon])

    for ability in model["abilities"]:
        if not ability in abilities_db.keys:
            raise Exception(f"Could not find ability id {ability} in the abilities database")
        m.abilities.append(abilities_db[ability])

    for faction_kw in model["faction_keywords"]:
        if not faction_kw in faction_keywords_db.keys:
            raise Exception(f"Could not find faction keyword id {faction_kw} in the faction keywords database")
        m.faction_keywords.append(faction_keywords_db[faction_kw])

    for kw in model["keywords"]:
        if not kw in keywords_db.keys:
            raise Exception(f"Could not find keyword id {kw} in the keywords database")
        m.keywords.append(keywords_db[kw])

    return m