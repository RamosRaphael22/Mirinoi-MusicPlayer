import random

class QueueManager:
    def __init__(self):
        self.queue = []
        self.original_queue = []   # 🔹 guarda ordem original
        self.current_index = 0

    def set_queue(self, tracks):
        self.queue = tracks.copy()
        self.original_queue = tracks.copy()  # 🔹 salva ordem original
        self.current_index = 0

    def current(self):
        if not self.queue:
            return None
        return self.queue[self.current_index]

    def next(self):
        if not self.queue:
            return None
        self.current_index = (self.current_index + 1) % len(self.queue)
        return self.current()

    def prev(self):
        if not self.queue:
            return None
        self.current_index = (self.current_index - 1) % len(self.queue)
        return self.current()

    def shuffle(self):
        if not self.queue:
            return

        # 🔹 mantém a música atual
        current = self.current()
        random.shuffle(self.queue)

        if current in self.queue:
            self.current_index = self.queue.index(current)
        else:
            self.current_index = 0

    # 🔹 Restaura ordem original
    def unshuffle(self):
        if not self.original_queue:
            return

        current = self.current()
        self.queue = self.original_queue.copy()

        if current in self.queue:
            self.current_index = self.queue.index(current)
        else:
            self.current_index = 0

    def clear(self):
        self.queue.clear()
        self.original_queue.clear()
        self.current_index = 0
