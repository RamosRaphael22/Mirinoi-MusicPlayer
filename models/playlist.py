# Model representing a playlist with ID, name, and URL
# Provides methods to convert to/from dict for CSV/JSON storage
# Each playlist has a unique integer ID, a name, and a URL
class Playlist:
    def __init__(self, id: int, name: str, url: str):
        self.id = id
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            name=data["name"],
            url=data["url"]
        )