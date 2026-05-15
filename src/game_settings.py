from dataclasses import dataclass


# is_walls


FIELD_MIN_WIDTH = 10           # change
FIELD_MAX_WIDTH = 100
FIELD_DEFAULT_WIDTH = 25

FIELD_MIN_HEIGHT = 7          # change
FIELD_MAX_HEIGHT = 70
FIELD_DEFAULT_HEIGHT = 17

MIN_PERCENT = 1               # change
MAX_PERCENT = 50
DEFAULT_PERCENT = 15


@dataclass
class GameSettings:
    width: int = FIELD_DEFAULT_WIDTH
    height: int = FIELD_DEFAULT_HEIGHT
    percent: int = DEFAULT_PERCENT


def read_game_settings(width_str, height_str, percent_str):
    try:
        width = int(width_str.strip())
        height = int(height_str.strip())
        percent = int(percent_str.strip())
    except ValueError:
        return None, "Введите целые числа"

    if not FIELD_MIN_WIDTH <= width <= FIELD_MAX_WIDTH:
        return None, f"Ширина должна быть от {FIELD_MIN_WIDTH} до {FIELD_MAX_WIDTH}"
    if not FIELD_MIN_HEIGHT <= height <= FIELD_MAX_HEIGHT:
        return None, f"Высота должна быть от {FIELD_MIN_HEIGHT} до {FIELD_MAX_HEIGHT}"
    if not MIN_PERCENT <= percent <= MAX_PERCENT:
        return None, f"Процент мин должен быть от {MIN_PERCENT} до {MAX_PERCENT}"

    return GameSettings(width, height, percent), ""
