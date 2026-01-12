# models/playlist.py
class Playlist:
    def __init__(self, id: int, name: str, url: str):
        self.id = id
        self.name = name
        self.url = url

    def to_dict(self):
        """Retorna um dict para salvar em CSV ou JSON"""
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
