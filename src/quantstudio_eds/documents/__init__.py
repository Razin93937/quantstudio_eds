from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from zipfile import ZipFile

from . import platesetup


@dataclass(frozen=True)
class Doc:
    paths: list[str]
    optional: bool
    present: Callable[[ZipFile], bool]
    parse: Callable[[ZipFile], Any]


DOCS = {
    platesetup.NAME: Doc(
        paths=platesetup.PATHS,
        optional=True,
        present=platesetup.present,
        parse=platesetup.parse,
    ),
}
