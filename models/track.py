# models/track.py
class Track:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def to_dict(self):
        """Para exibir na TrackList ou salvar em fila"""
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