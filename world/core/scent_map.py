# world/core/scent_map.py

class ScentMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scent = {}  # {(x, y): {"food": float, "corpse": float}}

    def emit(self, x, y, scent_type: str, intensity=5, radius=6):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dist = abs(dx) + abs(dy)
                if dist > radius:
                    continue
                tx, ty = x + dx, y + dy
                if not self.in_bounds(tx, ty):
                    continue
                level = max(intensity - dist, 0)
                if level <= 0:
                    continue
                scent_cell = self.scent.setdefault((tx, ty), {})
                scent_cell[scent_type] = scent_cell.get(scent_type, 0) + level

    def decay(self, decay_rate=0.95, threshold=0.01):
        to_delete = []
        for pos, scent in self.scent.items():
            for k in list(scent):
                scent[k] *= decay_rate
                if scent[k] < threshold:
                    del scent[k]
            if not scent:
                to_delete.append(pos)
        for p in to_delete:
            del self.scent[p]

    def get(self, x, y):
        return self.scent.get((x, y), {})

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
