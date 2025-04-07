class InfoPacket:
    def __init__(self, type, data, priority=1.0, ttl=150):
        self.type = type
        self.data = data
        self.priority = priority
        self.ttl = ttl  # Время жизни информации

    def decay(self):
        """ Уменьшает ttl и возвращает True, если пора забыть """
        self.ttl -= 1
        return self.ttl <= 0
