from dataclasses import dataclass
from typing import Any


@dataclass
class Setting:
    name: str
    value: Any

    def __repr__(self):
        return f"Setting(name={self.name}, value={self.value})"


@dataclass
class SettingsGroup:
    setting_type: str
    settings: list[Setting]

    def __repr__(self):
        settings_repr = ", ".join(repr(s) for s in self.settings)
        return f"SettingsGroup(group_name={self.setting_type}, settings=[{settings_repr}])"
