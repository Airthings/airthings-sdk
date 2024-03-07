from enum import Enum


class GetMultipleSensorsUnit(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"

    def __str__(self) -> str:
        return str(self.value)
