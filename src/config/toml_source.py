from typing import Any

import toml
from pydantic.fields import FieldInfo
from pydantic_settings import PydanticBaseSettingsSource


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        try:
            with open("config.toml") as f:
                config = toml.load(f)
            field_value = config.get(field_name)
            if field_value:
                return field_value, field_name, False
        except FileNotFoundError:
            pass
        return None, field_name, True
