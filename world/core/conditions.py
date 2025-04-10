# world/core/conditions.py

class WorldConditions:
    def __init__(self):
        self.data = {
            "humidity": 0.5,
            "temperature": 0.5,
            "sound_level": 0.0,
        }

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        return f"<Conditions {self.data}>"
