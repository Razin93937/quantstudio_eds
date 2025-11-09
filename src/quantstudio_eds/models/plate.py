from dataclasses import dataclass
from typing import ClassVar

from quantstudio_eds.models.well import Well


@dataclass
class PlateKind:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "type": "Type",
        "row_count": "RowCount",
        "column_count": "ColumnCount",
    }
    row_count: int
    column_count: int
    name: str = ""
    type: str = ""


class Plate:
    MAPPINGS: ClassVar[dict] = {
        "name": "Name",
        "description": "Description",
        "rows": "Rows",
        "columns": "Columns",
        "barcode": "Barcode",
    }

    def __init__(
        self,
        rows: int,
        columns: int,
        plate_kind: PlateKind,
        name: str = "",
        description: str = "",
        barcode: str | None = None,
    ):
        self.name = name
        self.description = description
        self.rows = rows
        self.columns = columns
        self.plate_kind = plate_kind
        self.barcode = barcode
        self.wells: dict[int, Well] = {}

    def add_well(self, well: Well):
        self.wells[well.well_index] = well

    def __repr__(self):
        return f"""Plate(name={self.name}, description={self.description},
    rows={self.rows}, columns={self.columns}, plate_kind={self.plate_kind}"""
