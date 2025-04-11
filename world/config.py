# world/config.py

# === Размеры карты ===
MAP_WIDTH = 50
MAP_HEIGHT = 50
TILE_SIZE = 16

# === Типы тайлов ===
TILE_TYPES = {
    "GROUND": 0,
    "ROCK": 1,
    "NEST": 2,
    "FOOD": 3,
    "STICK": 4,
    "CORPSE": 5,
}

# === Цвета тайлов (для отрисовки / отладки) ===
TILE_COLORS = {
    TILE_TYPES["GROUND"]: (139, 69, 19),
    TILE_TYPES["ROCK"]: (100, 100, 100),
    TILE_TYPES["NEST"]: (255, 223, 0),
    TILE_TYPES["FOOD"]: (0, 200, 0),
    TILE_TYPES["STICK"]: (139, 69, 19),
    TILE_TYPES["CORPSE"]: (150, 0, 0),
}

# === Цвета объектов, агентов, UI ===
COLOR_BG = (0, 0, 0)
COLOR_AGENT = (255, 255, 255)
COLOR_OBJECT_FOOD = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)


# === Физические свойства тайлов ===
TILE_PASSABLE = {
    TILE_TYPES["GROUND"]: True,
    TILE_TYPES["ROCK"]: False,
    TILE_TYPES["NEST"]: True,
    TILE_TYPES["FOOD"]: True,
    TILE_TYPES["STICK"]: False,  # Пока считаем как блокирующий объект
    TILE_TYPES["CORPSE"]: True,
}

TILE_OPAQUE = {
    TILE_TYPES["GROUND"]: False,
    TILE_TYPES["ROCK"]: True,
    TILE_TYPES["NEST"]: False,
    TILE_TYPES["FOOD"]: False,
    TILE_TYPES["STICK"]: False,
    TILE_TYPES["CORPSE"]: False,
}


# === Направления движения (8 направлений) ===
DIRECTIONS = {
    "N":  (0, -1),
    "NE": (1, -1),
    "E":  (1, 0),
    "SE": (1, 1),
    "S":  (0, 1),
    "SW": (-1, 1),
    "W":  (-1, 0),
    "NW": (-1, -1),
}
DIRECTION_LIST = list(DIRECTIONS.values())

# === Сенсоры ===
VISION_RANGE = 3
SCENT_RADIUS = 6

# === Энергия и параметры агентов ===
STARTING_ENERGY = 100
HUNGER_DEATH_THRESHOLD = 200

ENERGY_LOSS_PER_TICK = 1
ENERGY_GAIN_PER_FOOD = 40
ENERGY_GAIN_IF_EAT_IN_NEST = 40
ENERGY_GAIN_IF_EAT_OUTSIDE = 10

# === Генерация карты ===
DEFAULT_SEED = 1
OBSTACLE_DENSITY = 0.1
FOOD_DENSITY = 0.15
MAX_KNOWN_COLONIES = 4

# === Поведение мира ===
TICKS_PER_GENERATION = 1000

# === Заглушки для условий среды ===
WORLD_CONDITIONS = {
    "humidity": 0.5,
    "temperature": 0.5,
    "sound_level": 0.0
}

# === Режим отладки ===
DEBUG_MODE = True
DEBUG_SHOW_SCENT = True
