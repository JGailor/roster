import xml.sax
import json

class BattlescribeCatSchema(xml.sax.ContentHandler):
    def __init__(self):
        self.tree = {"attrs": [], "children": {}}
        self.stack = []
        self.indent = 0

    def startElement(self, name, attrs):
        cur_node = self.tree
        for node in self.stack:
            if cur_node["children"].get(node, None):
                cur_node = cur_node["children"].get(node)
            else:
                raise Exception(f"Did not recurse into the tree to find the last child of {self.stack}, {self.tree}")

        attr_names = list(map(lambda x: x[0], attrs.items()))

        if cur_node["children"].get(name, None):
            prev_attr_names = cur_node["children"][name]["attrs"]
            cur_node["children"][name]["attrs"] = list(set(attr_names) | set(prev_attr_names))
        else:
            cur_node["children"][name] = {"attrs": attr_names, "children": {}}

        self.stack.append(name) 

    def endElement(self, name):
        if not name == self.stack[-1]:
            raise Exception(f"Our stack has broken: the end element {name} was found but the top of the stack was {self.stack[-1]}")
        self.stack.pop()

    @property
    def schema_tree(self):
        return self.tree

    def print(self):
        json.dumps(self.tree)
