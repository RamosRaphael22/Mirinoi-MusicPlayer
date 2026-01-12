import random


class QueueManager:
    def __init__(self):
        self.queue = []
        self.current_index = 0

    def set_queue(self, tracks):
        self.queue = tracks.copy()
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
        random.shuffle(self.queue)
        self.current_index = 0
