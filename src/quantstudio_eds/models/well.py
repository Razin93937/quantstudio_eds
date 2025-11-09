from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Detector:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "assay_id": "AssayID",
        "reporter": "Reporter",
        "quencher": "Quencher",
        "color": "Color",
    }
    name: str
    reporter: str
    quencher: str
    color: str
    assay_id: str | None = None


@dataclass(frozen=True)
class DetectorTask:
    detector: Detector
    task: str
    concentration: str


@dataclass(frozen=True)
class SampleFeature:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "color": "Color",
        "custom_property": "CustomProperty",
    }
    name: str
    color: str
    custom_property: str | None = None


@dataclass(frozen=True)
class Allele:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "reporter": "Reporter",
        "quencher": "Quencher",
        "color": "Color",
    }
    name: str
    reporter: str
    quencher: str
    color: str


@dataclass(frozen=True)
class Marker:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "color": "Color",
    }
    name: str
    color: str
    alleles: list[Allele]


@dataclass(frozen=True)
class MarkerTask:
    marker: Marker
    task: str


class Well:
    def __init__(self, well_index: int, is_omit: bool):
        self.well_index = well_index
        self.is_omit = is_omit

    def add_detector_task(self, detector_task: DetectorTask):
        if not hasattr(self, "detector_tasks"):
            self.detector_tasks = []
        self.detector_tasks.append(detector_task)

    def add_sample_feature(self, sample: SampleFeature):
        if not hasattr(self, "samples"):
            self.samples = []
        self.samples.append(sample)

    def add_marker_task(self, marker_task: MarkerTask):
        if not hasattr(self, "marker_tasks"):
            self.marker_tasks = []
        self.marker_tasks.append(marker_task)

    def __repr__(self):
        return f"""Well(index={self.well_index}, is_omit={self.is_omit},
    detector_tasks={getattr(self, "detector_tasks", [])},
    samples={getattr(self, "samples", [])},
    marker_tasks={getattr(self, "marker_tasks", [])})"""
