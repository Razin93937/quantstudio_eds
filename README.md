# quantstudio-eds

A python wrapper for reading Applied Biosystems QuantStudio `.eds` files.

## Table of Contents

- [Features](##Features)
- [Quickstart](#quickstart)
- [Examples](#examples)

## Features

- Parse QuantStudio .eds archives without extracting files.
- Read plate layout (plate_setup.xml) into Plate/Well model objects.
- Read multicomponent fluorescence data (multicomponentdata.xml) into per-well dye intensity arrays.

## Quickstart

```python
from quantstudio_eds.io import EDSZip
from quantstudio_eds.documents.platesetup import parse as parse_platesetup
from quantstudio_eds.documents.multicomponentdata import parse as parse_multicomponent

with EDSZip("path/to/file.eds") as eds:
    plate = parse_platesetup(eds)                    # returns Plate
    plate = parse_multicomponent(eds, plate)         # fills Plate with dyes/temperatures
```

## Examples

Read plate setup and dye data:

```python
from quantstudio_eds.io import EDSZip
from quantstudio_eds.documents import platesetup, multicomponentdata

with EDSZip("tests/eds_files/example.eds") as eds:
    plate = platesetup.parse(eds)
    plate = multicomponentdata.parse(eds, plate)

# Inspect first well
w = plate.wells[0]
print(w.well_index, w.is_omit, getattr(w, "dyes", []))
```
