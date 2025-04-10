# world/systems/logger.py

class Logger:
    def __init__(self):
        self.events = []

    def log(self, tick: int, event_type: str, data: dict):
        """
        Сохраняет событие в формате:
        {"tick": 12, "event": "agent_died", "id": 3}
        """
        entry = {
            "tick": tick,
            "event": event_type,
            **data
        }
        self.events.append(entry)

    def get_events(self):
        return self.events

    def clear(self):
        self.events.clear()
