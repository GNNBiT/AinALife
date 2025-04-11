# world/core/scent_map.py

class ScentPacket:
    def __init__(self, scent_type: str, colony_id: int, intensity: float = 1.0, lifespan: int = 10, direction=None):
        self.type = scent_type        # "food", "danger", "trail", "corpse", "fake" и т.д.
        self.colony_id = colony_id    # Кто оставил запах (внутреннее поле)
        self.intensity = intensity    # Сила запаха
        self.lifespan = lifespan      # Остаточное время жизни
        self.direction = direction    # Вектор направления (опционально)

class ScentMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scent = {}  # {(x, y): [ScentPacket, ScentPacket, ...]}

    def emit(self, x, y, scent_type: str, colony_id: int, intensity=5, radius=6, lifespan=10, direction=None):
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

                scent_packet = ScentPacket(
                    scent_type=scent_type,
                    colony_id=colony_id,
                    intensity=level,
                    lifespan=lifespan,
                    direction=(-dx, -dy) if direction is None else direction
                )

                self.scent.setdefault((tx, ty), []).append(scent_packet)

    def decay(self, decay_rate=0.95, threshold=0.01):
        to_delete = []
        for pos, packet_list in self.scent.items():
            new_packets = []
            for packet in packet_list:
                packet.intensity *= decay_rate
                packet.lifespan -= 1
                if packet.intensity >= threshold and packet.lifespan > 0:
                    new_packets.append(packet)
            if new_packets:
                self.scent[pos] = new_packets
            else:
                to_delete.append(pos)
        for p in to_delete:
            del self.scent[p]

    def get(self, x, y) -> list:
        return self.scent.get((x, y), [])

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
