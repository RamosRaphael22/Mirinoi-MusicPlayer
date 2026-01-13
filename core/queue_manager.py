import random

# Manages the playback queue of tracks
# Supports setting the queue, navigating tracks, shuffling, and unshuffling
# Maintains the original order of tracks for unshuffling
# Provides methods to get the current, next, and previous tracks
# Allows clearing the queue
# Uses random.shuffle for shuffling the queue
# Keeps track of the current index in the queue
# Allows wrapping around the queue when navigating next/previous
# Preserves the original queue order for unshuffling
class QueueManager:
    def __init__(self):
        self.queue = []
        self.original_queue = []  
        self.current_index = 0

    def set_queue(self, tracks):
        self.queue = tracks.copy()
        self.original_queue = tracks.copy()  
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

        current = self.current()
        random.shuffle(self.queue)

        if current in self.queue:
            self.current_index = self.queue.index(current)
        else:
            self.current_index = 0

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
