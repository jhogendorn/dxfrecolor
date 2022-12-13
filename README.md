# DXF Recolorer

### The Problem

Lightburn uses DXF layer colors on import to define separate layers, not the layer definitions themselves. Fusion360 does not define different colors in dxf outputs. This is a pain when working with folded sheet metal drawings with a flat pattern output that contains bend lines.

### The Solution

This script uses ezdxf to grab each defined layer and assign it a different color.

It will also nicely draw it for you at the end to let you validate.

## Install

1. `git clone <thisrepo>`
2. `python -m venv .venv`
3. `pip install -r requirements.txt`
4. `python prep.py path/to/my.dxf`
