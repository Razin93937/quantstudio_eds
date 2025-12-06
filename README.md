# quantstudio-eds

A python wrapper for reading Applied Biosystems QuantStudio `.eds` files.

## Table of Contents

- [quantstudio-eds](#quantstudio-eds)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Quickstart](#quickstart)
  - [Examples](#examples)

## Features

- Parse QuantStudio .eds archives without extracting files.
- Read plate layout (plate_setup.xml) into Plate/Well model objects.
- Read multicomponent fluorescence data (multicomponentdata.xml) into per-well dye intensity arrays.
- Read analysis protocol settings (analysis_protocol.xml) into SettingsGroup/Setting model objects.

## Quickstart

```python
from quantstudio_eds.io import EDSZip
from quantstudio_eds.documents.platesetup import parse as parse_platesetup
from quantstudio_eds.documents.multicomponentdata import parse as parse_multicomponent
from quantstudio_eds.documents.analysisprotocol import parse as parse_analysisprotocol

with EDSZip("path/to/file.eds") as eds:
    plate = parse_platesetup(eds)                    # returns Plate
    plate = parse_multicomponent(eds, plate)         # fills Plate with dyes/temperatures
    plate = parse_analysisprotocol(eds, plate)       # fills Plate with analysis protocol settings
```

## Examples

Read plate setup, dye data, and analysis protocol:

```python
from quantstudio_eds.io import EDSZip
from quantstudio_eds.documents import platesetup, multicomponentdata, analysisprotocol

with EDSZip("tests/eds_files/example.eds") as eds:
    plate = platesetup.parse(eds)
    plate = multicomponentdata.parse(eds, plate)
    plate = analysisprotocol.parse(eds, plate)

# Inspect first well
w = plate.wells[0]
print(w.well_index, w.is_omit, getattr(w, "dyes", []))

# Inspect analysis protocol settings
if hasattr(plate, 'analysis_protocol'):
    for group in plate.analysis_protocol:
        print(f"Group: {group.setting_type}")
        for setting in group.settings:
            print(f"  {setting.name}: {setting.value}")
```
