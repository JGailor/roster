#!/bin/env python
import sys
import os
import xml.sax

# Append the higher-level directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from w40k.battlescribe.schema import BattlescribeCatSchema

if len(sys.argv) < 2:
    print("usage: python bin/dump_battlescribe_schema.py <battlescribe-filename> [outputformat (json, html)]")
    sys.exit(-1)

handler = BattlescribeCatSchema()
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
with open(sys.argv[1]) as f:
    parser.parse(sys.argv[1])

html = "<html><head><title>Battlescribe .cat Schema</title><style>"
html += ".element-line:nth-child(even) {background: #CCC;}"
html += ".element {color: #FF851B; font-weight: bold;}"
html += ".attr-open-paren {margin-left: 10px;}"
html += ".attr.first {margin-left: 0px;}"
html += ".attr {margin-left: 5px; color: #001f3f; font-style: italic;}"
html += "</style></head><body>"

def render_node(name, attrs, children, indent):
    html = f"<div class=\"element-line\" style=\"margin-left: {indent * 10}px;padding: 5px;\"><span class=\"element\">{name}</span>"
    html += "<span class=\"attr-open-paren\">(</span>"
    if len(attrs) > 0:
        html += "<span class=\"attr first\">" + "</span>, <span class=\"attr\">".join(sorted(attrs)) + "</span>"
    html += "<span>)</span></div>"
    for name, node in children.items():
        html += render_node(name, node["attrs"], node["children"], indent + 1)
    return html

for name, node in handler.tree["children"].items():
    html += render_node(name, node["attrs"], node["children"], 0)

print(html)


