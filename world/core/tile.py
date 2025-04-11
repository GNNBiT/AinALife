from world.config import TILE_PASSABLE, TILE_OPAQUE
from world.entities.object import Barricade, Stick


class Tile:
    def __init__(self, tile_type: int):
        self.type = tile_type
        self.passable = TILE_PASSABLE.get(tile_type, True)
        self.opaque = TILE_OPAQUE.get(tile_type, False)
        self.objects = {}  # Ключ — тип объекта, значение — объект или количество

    def is_empty(self) -> bool:
        """Проверяет, пустая ли клетка"""
        return len(self.objects) == 0

    def can_enter(self) -> bool:
        if not self.passable:
            return False
        for obj in self.objects.values():
            if obj.blocks_movement():
                return False
        return True

    def set_object(self, obj):
        obj_type = obj.__class__.__name__
        # Если в клетке уже что-то есть и это не того же типа — отказ
        if obj_type in self.objects:
            existing = self.objects[obj_type]
            if not existing.stackable:
                return False  # уже есть и не стакуется
            if hasattr(existing, "amount"):
                existing.amount += 1
            return True
        # если есть другой объект — отказ
        if len(self.objects) > 0:
            return False
        # просто добавить
        self.objects[obj_type] = obj
        return True

    def remove_object(self, obj):
        """Удалить объект из клетки"""
        obj_type = obj.__class__.__name__
        if obj_type in self.objects:
            existing = self.objects[obj_type]
            if existing.stackable:
                if hasattr(existing, "remove_one"):
                    if existing.remove_one():
                        del self.objects[obj_type]
            else:
                del self.objects[obj_type]  # Удаляем нестакуемый объект
            return True
        return False

    def place_stick(self):
        """Добавить ветку, если 3 ветки — сделать баррикадой"""
        if "Stick" in self.objects:
            stick = self.objects["Stick"]
            if stick.add_one():
                self.set_object(Barricade())  # Заменяем на баррикаду
        elif not self.is_empty():
            self.set_object(Stick())  # Установить палку, если клетка пустая

    def __repr__(self):
        return f"<Tile type={self.type} opaque={self.opaque} objects={self.objects}>"
