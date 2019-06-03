from __future__ import annotations
from typing import Dict

import xml.etree.ElementTree as ET

ns_map: Dict[str, str] = {
    "cs": "http://www.battlescribe.net/schema/catalogueSchema"
}

class BattlescribeCatFile:
    def __init__(self, fname: str):
        self.tree = ET.parse(fname)
        self.root = self.tree.getroot()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def publications(self):
        publications = []
        for p in self._findall("./cs:publications/cs:publication"):
            publications.append({"id": p.get("id"), "name": p.get("name")})
        return publications

    @property
    def profile_types(self):
        profile_types = []
        for pt in self._findall("./cs:profileTypes/cs:profileType"):
            d = {"id": pt.get("id"), "name": pt.get("name"), "characteristic_types": []}
            for ct in self._findall("./cs:characteristicTypes/cs:characteristicType", pt):
                d["characteristic_types"].append({"id": ct.get("id"), "name": ct.get("name")})
            profile_types.append(d)
        return profile_types

    @property
    def category_entries(self):
        category_entries = []
        for ce in self._findall("./cs:categoryEntries/cs:categoryEntry"):
            category_entries.append({
                "id": ce.get("id"),
                "name": ce.get("name"),
                "hidden": self._bool(ce.get("hidden"))
            })
        return category_entries

    @property
    def entry_links(self):
        entry_links = []
        for el in self._findall("./cs:entryLinks/cs:entryLink"):
            entry_links.append({
                "id": el.get("id"),
                "name": el.get("name"),
                "hidden": self._bool(el.get("hidden")),
                "collective": self._bool(el.get("collective")),
                "target_id": el.get("targetId"),
                "type": el.get("type"),
                "category_links": self._category_links(el) 
            })
        return entry_links
    
    @property
    def rules(self):
        rules = []
        for r in self._findall("./cs:rules/cs:rule"):
            rules.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "hidden": self._bool(r.get("hidden")),
                "description": self._nodeText(self._find("./cs:description", r))
            }) 
        return rules

    @property
    def info_links(self):
        return self._info_links()

    @property
    def shared_selection_entries(self):
        sses = []
        for se in self._findall("./cs:sharedSelectionEntries/cs:selectionEntry"):
            sses.append({
                "id": se.get("id"),
                "name": se.get("name"),
                "page": self._int(se.get("page")),
                "hidden": self._bool(se.get("hidden")),
                "collective": self._bool(se.get("collective")),
                "type": se.get("type"),
                "profiles": self._se_profiles(se),
                "info_links": self._info_links(se),
                "category_links": self._category_links(se),
                "entry_links": self._se_entry_links(se),
                "costs": self._se_costs(se)
            })
        return sses

    @property
    def shared_selection_entry_groups(self):
        selector = "./cs:sharedSelectioEntryGroups/cs:selectionEntryGroup"
        selection_entry_groups = self._findall(selector)
        return map(self._selection_entry_group, selection_entry_groups)

    @property
    def shared_profiles(self):
        sps = []
        for p in self._findall("./cs:sharedProfiles/cs:profile"):
            sps.append(self._sp_profile(p))
        return sps

    def _findall(self, selector:str, root=None):
        return (root or self.root).findall(selector, ns_map)

    def _find(self, selector: str, root=None):
        return (root or self.root).find(selector, ns_map)

    def _nodeText(self, node, default=""):
        return node.text if not node == None else default

    def _bool(self, val: str) -> bool:
        return True if val == "true" else False
    
    def _int(self, val: str) -> int:
        try:
            return int(val)
        except:
            return None
    
    def _float(self, val: str) -> float:
        return float(val)

    def _category_links(self, root=None):
        category_links = []
        for cl in self._findall("./cs:categoryLinks/cs:categoryLink", root):
            hidden = self._bool(cl.get("hidden"))
            primary = self._bool(cl.get("primary"))
            d = { 
                "id": cl.get("id"),
                "name": cl.get("name"),
                "hidden": hidden,
                "target_id": cl.get("targetId"),
                "primary": primary
            }
            category_links.append(d)
        return category_links

    def _info_links(self, root=None):
        info_links = []
        for il in self._findall("./cs:infoLinks/cs:infoLink", root):
            info_links.append({
                "id": il.get("id"),
                "name": il.get("name"),
                "hidden": self._bool(il.get("hidden")),
                "target_id": il.get("targetId"),
                "type": il.get("type")
            })
        return info_links 

    def _se_profiles(self, root):
        seps = []
        for p in self._findall("./cs:profiles/cs:profile", root):
            d = {
                "id": p.get("id"),
                "name": p.get("name"),
                "hidden": self._bool(p.get("hidden")),
                "type_id": p.get("typeId"),
                "type_name": p.get("typeName"),
                "characteristics": self._se_profile_characteristics(p)
            }
            seps.append(d)
        return seps

    def _se_profile_characteristics(self, root):
        cs = []
        for c in self._findall("./cs:characteristics/cs:characteristic", root):
            cs.append({"name": c.get("name"), "type_id": c.get("typeId"), "value": c.text})
        return cs

    def _se_category_links(self, root):
        cls = []
        for cl in self._findall("./cs:categoryLinks/cs:categoryLink", root):
            cls.append({
                "id": cl.get("id"),
                "name": cl.get("name"),
                "hidden": self._bool(cl.get("hidden")),
                "target_id": cl.get("targetId"),
                "primary": self._bool(cl.get("primary"))
            })
        return cls

    def _se_entry_links(self, root):
        els = []
        for el in self._findall("./cs:entryLinks/cs:entryLink", root):
            els.append({
                "id": el.get("id"),
                "name": el.get("name"),
                "hidden": self._bool(el.get("hidden")),
                "target_id": el.get("targetId"),
                "primary": self._bool(el.get("primary")),
                "constraints": self._se_entry_link_constraints(el)
            })
        return els

    def _se_entry_link_constraints(self, root):
        cs = []
        for c in self._findall("./cs:constraints/cs:constraint", root):
            cs.append({
                "id": c.get("id"),
                "field": c.get("field"),
                "scope": c.get("parent"),
                "value": c.get("value"),
                "percent_value": self._bool(c.get("percentValue")),
                "shared": self._bool(c.get("shared")),
                "include_child_selections": self._bool(c.get("includeChildSelections")),
                "include_child_forces": self._bool(c.get("includeChildForces")),
                "type": c.get("type")
            })
        return cs
    
    def _se_costs(self, root):
        cs = []
        for c in self._findall("./cs:costs/cs:cost", root):
            cs.append({
                "name": c.get("name"),
                "type_id": c.get("typeId"),
                "value": self._float(c.get("value"))
            })
        return cs

    def _selection_entry_group(self, root):
        constraints = self._findall("./cs:constraints/cs:constraint", root)
        sub_segs = self._findall("./cs:selectionEntryGroups/cs:selectionEntryGroup", root)
        entry_links = self._findall("./cs:entryLinks/cs:entryLink", root)
        modifiers = self._findall("./cs:modifiers/cs:modifier", root)
        return {
            "id": root.get("id"),
            "name": root.get("name"),
            "hidden": self._bool(root.get("hidden")),
            "collective": self._bool(root.get("collective")),
            "default_selection_entry_id": root.get("defaultSelectionEntryId"),
            "constraints": list(map(self._seg_constraint, constraints)),
            "selection_entry_groups": list(map(self._selection_entry_group, sub_segs)),
            "entry_links": list(map(self._seg_entry_link, entry_links)),
            "modifiers": list(map(self._seg_modifier, modifiers))
        }

    def _seg_constraint(self, root):
        return {
            "id": root.get("id"),
            "field": root.get("field"),
            "scope": root.get("scope"),
            "value": root.get("value"),
            "percent_value": self._bool(root.get("percentValue")),
            "shared": self._bool(root.get("shared")),
            "include_child_selections": self._bool(root.get("includeChildSelections")),
            "include_child_forces": self._bool(root.get("includeChildForces")),
            "type": root.get("type")
        }

    def _seg_entry_link(self, root):
        modifiers = self._findall("./cs:modifiers/cs:modifier", root)
        return {
            "id": root.get("id"),
            "name": root.get("name"),
            "hidden": self._bool(root.get("hidden")),
            "collective": self._bool(root.get("collective")),
            "target_id": root.get("targetId"),
            "type": root.get("type"),
            "modifiers": list(map(self._seg_modifier, modifiers))
        }

    def _seg_modifier(self, root):
        conditions = self._findall("./cs:conditions/cs:condition", root)
        return {
            "type": root.get("type"),
            "field": root.get("field"),
            "value": root.get("value"),
            "conditions": list(map(self._seg_el_m_condition, conditions))
        }

    def _seg_el_m_condition(self, root):
        return {
            "field": root.get("field"),
            "scope": root.get("scope"),
            "value": root.get("value"),
            "percent_value": self._bool(root.get("percentValue")),
            "shared": self._bool(root.get("shared")),
            "include_child_selections": self._bool(root.get("includeChildSelections")),
            "include_child_forces": self._bool(root.get("includeChildForces")),
            "child_id": root.get("childId"),
            "type": root.get("type")
        }

    def _sp_profile(self, root):
        return {
            "id": root.get("id"),
            "name": root.get("name"),
            "hidden": self._bool(root.get("hidden")),
            "type_id": root.get("typeId"),
            "type_name": root.get("typeName"),
            "characteristics": self._sp_p_characteristics(root)
        }

    def _sp_p_characteristics(self, root):
        return map(self._sp_p_characteristic, self._findall("./cs:characteristics/cs:characteristic"))
    
    def _sp_p_characteristic(self, root):
        return {
            "name": root.get("name"),
            "type_id": root.get("typeId"),
        }

        