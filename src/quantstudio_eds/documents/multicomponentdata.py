import re

from quantstudio_eds.io import EDSZip
from quantstudio_eds.models.plate import Plate
from quantstudio_eds.models.well import Dye

from .utils import clean_string, parse_bracketed_floats, parse_bracketed_ints, parse_bracketed_list

NAME = "multicomponentdata"
PATHS = ["apldbio/sds/multicomponentdata.xml"]


def present(z: EDSZip) -> bool:
    return z.exists(PATHS[0])


def _parse_collection_points(text: str) -> list[dict]:
    """
    Parses strings like:
    [[Stg:2 Cyc:1 Stp:2 Pt:1], [Stg:2 Cyc:2 Stp:2 Pt:1], ...]
    into list of dicts: [{"stage":2,"cycle":1,"step":2,"point":1}, ...]
    """
    if not text:
        return []
    # find all occurrences of Stg:x Cyc:y Stp:z Pt:w
    pattern = re.compile(r"Stg:(\d+)\s+Cyc:(\d+)\s+Stp:(\d+)\s+Pt:(\d+)")
    return [
        {"stage": int(a), "cycle": int(b), "step": int(c), "point": int(d)}
        for (a, b, c, d) in pattern.findall(text)
    ]


def parse(z: EDSZip, plate: Plate) -> Plate:
    root = z.read_and_parse_xml(PATHS[0])
    well_count = int(root.findtext(".//WellCount"))
    cycle_count = int(root.findtext(".//CycleCount"))
    tc_stage_flags = parse_bracketed_ints(root.findtext(".//TCStageFlags"))
    collection_points = _parse_collection_points(root.findtext(".//CollectionPoints"))

    plate.set_multicomponent_data(cycle_count, tc_stage_flags, collection_points)

    temps_text = root.findtext(".//SampleTemperatures") or ""
    temps_list = [float(tok) for tok in temps_text.split() if tok.strip()]
    # reshape to well_count x cycle_count
    temps_list = [temps_list[i : i + cycle_count] for i in range(0, len(temps_list), cycle_count)]

    for i, well in enumerate(plate.wells.values()):
        well.sample_temperatures = temps_list[i]

    for value in root.xpath(".//DyeData"):
        well_index = int(value.get("WellIndex"))
        promoters = parse_bracketed_list(value.findtext("DyeList"))
        if not promoters or promoters == [""]:
            continue
        for i, promoter in enumerate(promoters):
            cycle_data = root.findall(f".//SignalData[@WellIndex='{well_index}']/CycleData")[i]
            intensities = parse_bracketed_floats(cycle_data.text)
            plate.wells[well_index].add_dye(Dye(clean_string(promoter), intensities))

    if well_count != len(plate.wells):
        print(f"Warning: Well count mismatch. Expected {well_count}, got {len(plate.wells)}")

    return plate
