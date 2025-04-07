from enum import Enum

class Direction(Enum):
    N  = (0, -1)
    NE = (1, -1)
    E  = (1, 0)
    SE = (1, 1)
    S  = (0, 1)
    SW = (-1, 1)
    W  = (-1, 0)
    NW = (-1, -1)

    @staticmethod
    def all():
        return list(Direction)

    def turn_left(self):
        idx = Direction.all().index(self)
        return Direction.all()[(idx - 1) % 8]

    def turn_right(self):
        idx = Direction.all().index(self)
        return Direction.all()[(idx + 1) % 8]

    def to_vector(self):
        return self.value
