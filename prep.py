import sys
import argparse
import ezdxf
from ezdxf.entities import is_graphic_entity
from ezdxf import recover
#from ezdxf.commands import Draw

parser = argparse.ArgumentParser(
        "prep.py",
        description="DXF Layer Recolorererer",
    )
parser.add_argument(
            "file",
            metavar="FILE",
            help="DXF file to recolor",
        )

args = parser.parse_args(sys.argv[1:])
filename = args.file if args.file else 'test.dxf'

print(f"Loading {filename}")

loader = recover.readfile
try:
    doc, auditor = loader(filename)
except IOError:
    msg = "Not a DXF file or a generic I/O error."
    print(msg)
    sys.exit(2)
except ezdxf.DXFStructureError as e:
    msg = f"Invalid or corrupted DXF file: {str(e)}"
    print(msg)
    sys.exit(2)

if auditor.has_errors:
    auditor.print_error_report()
if auditor.has_fixes:
    auditor.print_fixed_errors()

if auditor.has_errors is False and auditor.has_fixes is False:
    print("No errors found.")
else:
    print(
        f"Found {len(auditor.errors)} errors, "
        f"applied {len(auditor.fixes)} fixes"
    )


msp = doc.modelspace()

layer_count = len(doc.layers)
print(f"Found {layer_count} layers")

# iteration
for layer in doc.layers:
    if layer.dxf.name != "0":
        print(f"Disabling Layer {layer.dxf.name}")
        layer.off()  # switch all layers off except layer "0"

all_layer_names = set([e.dxf.layer for e in doc.entitydb.values() if is_graphic_entity(e)])

i=0
step=1
offset=0
for name in all_layer_names:
    if name == "0":
        continue
    i += step
    aci = offset+i
    if name not in doc.layers:
        layer = doc.layers.add(name=name, color=aci)
        print(f"Created layer {name} as ACI:{aci}")
    else:
        layer = doc.layers.get(name)
        layer.color = aci
        print(f"Found layer {name}, set ACI:{aci}")
    layer.on()
    print(f"Enabled layer {name}")

from ezdxf.groupby import groupby
group = groupby(entities=msp, dxfattrib="layer")

for label, entities in group.items():
    #print(f'Layer "{label}" contains following entities:')
    for entity in entities:
        #print(f"    {entity} ({entity.dxf.color})")
        entity.dxf.color = 256
    #print("-"*40)

output = f"{filename}_output.dxf"
doc.saveas(output)

import subprocess

processes = []
commands = [
        ['ezdxf', 'view', output],
        ['ezdxf', 'browse', output],
        ]

for command in commands:
    p = subprocess.Popen(command)
    processes.append((p))

for p in processes:
    p.wait()
