# src/quantstudio_eds/io.py
from __future__ import annotations

from zipfile import Path as ZipPath
from zipfile import ZipFile


class EDSZip:
    """Context manager to access files inside an EDS (ZIP) without extracting."""

    def __init__(self, path: str):
        self._path = path
        self._zip: ZipFile | None = None

    def __enter__(self) -> EDSZip:
        self._zip = ZipFile(self._path)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._zip:
            self._zip.close()

    def read_text(self, inner: str, encoding="utf-8") -> str:
        assert self._zip is not None
        with self._zip.open(inner) as f:
            return f.read().decode(encoding)

    def exists(self, inner: str) -> bool:
        assert self._zip is not None
        return ZipPath(self._zip, inner).is_file()

    def read_and_parse_xml(self, inner: str):
        """Read and parse an XML file inside the ZIP."""
        from lxml import etree

        xml_content = self.read_text(inner)
        return etree.fromstring(xml_content.encode("utf-8"))
