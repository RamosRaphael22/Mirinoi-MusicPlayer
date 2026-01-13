import csv
import os
from typing import List
from models.playlist import Playlist

# Service to manage playlists stored in a CSV file
# Ensures CSV integrity, loads, adds, and removes playlists
# Backs up corrupted files
# CSV file format: id,name,url
# Each playlist has a unique integer ID
# Provides methods to load all playlists, add a new playlist, and remove an existing playlist by ID
# Backs up the original CSV file if headers are incorrect
# Creates a new CSV file with correct headers if the original is missing or corrupted
class CSVService:
    HEADERS = ["id", "name", "url"]

    def __init__(self, file_path: str = "playlists.csv"):
        self.file_path = os.path.abspath(file_path)
        self._ensure_csv_integrity()

    def _ensure_csv_integrity(self):
        if not os.path.exists(self.file_path):
            self._create_empty_csv()
            return

        with open(self.file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()

        if first_line.lower() != ",".join(self.HEADERS):
            backup = self.file_path + ".bak"
            os.rename(self.file_path, backup)
            self._create_empty_csv()

    def _create_empty_csv(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADERS)

    def load_playlists(self) -> List[Playlist]:
        playlists = []

        with open(self.file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    playlist = Playlist(
                        id=int(row["id"]),
                        name=row["name"],
                        url=row["url"]
                    )
                    playlists.append(playlist)
                except (KeyError, ValueError, TypeError):
                    continue

        return playlists

    def _get_next_id(self) -> int:
        playlists = self.load_playlists()
        return max((p.id for p in playlists), default=0) + 1

    def add_playlist(self, name: str, url: str) -> Playlist:
        new_playlist = Playlist(
            id=self._get_next_id(),
            name=name.strip(),
            url=url.strip()
        )

        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([new_playlist.id, new_playlist.name, new_playlist.url])

        return new_playlist

    def remove_playlist(self, playlist_id: int) -> bool:
        playlists = self.load_playlists()
        updated = [p for p in playlists if p.id != playlist_id]

        if len(updated) == len(playlists):
            return False

        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADERS)
            for p in updated:
                writer.writerow([p.id, p.name, p.url])

        return True