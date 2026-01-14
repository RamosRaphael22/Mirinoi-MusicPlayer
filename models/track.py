# Model representing a track with title and URL
# Provides methods to convert to/from dict for CSV/JSON storage
class Track:
    def __init__(self, title: str, url: str, artist: str | None = None):
        self.title = title
        self.artist = artist if artist else "Unknown Artist"
        self.url = url

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            artist=data.get("artist"),
            url=data["url"]
        )
