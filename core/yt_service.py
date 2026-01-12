import subprocess
import json
from typing import List, Dict


class YouTubeService:
    def __init__(self):
        self.ytdlp_cmd = "yt-dlp"

    # 🔹 Retorna músicas de uma playlist
    def get_tracks_from_playlist(self, playlist_url: str) -> List[Dict]:
        command = [
            self.ytdlp_cmd,
            "--flat-playlist",
            "--dump-json",
            playlist_url
        ]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8"
            )

            tracks = []

            for line in process.stdout:
                try:
                    data = json.loads(line)
                    track = {
                        "title": data.get("title"),
                        "id": data.get("id"),
                        "url": f"https://music.youtube.com/watch?v={data.get('id')}"
                    }

                    if track["title"] and track["id"]:
                        tracks.append(track)

                except json.JSONDecodeError:
                    continue

            process.wait()
            return tracks

        except FileNotFoundError:
            raise RuntimeError("yt-dlp não encontrado no PATH")

    # 🔹 Busca simples (opcional para depois)
    def search_first(self, query: str) -> Dict | None:
        command = [
            self.ytdlp_cmd,
            "--dump-json",
            f"ytsearch1:{query}"
        ]

        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8"
            )

            data = json.loads(output)
            return {
                "title": data.get("title"),
                "url": f"https://music.youtube.com/watch?v={data.get('id')}"
            }

        except Exception:
            return None
