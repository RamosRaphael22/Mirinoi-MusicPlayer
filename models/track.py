# Model representing a track with title and URL
# Provides methods to convert to/from dict for CSV/JSON storage
class Track:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            url=data["url"]
        )