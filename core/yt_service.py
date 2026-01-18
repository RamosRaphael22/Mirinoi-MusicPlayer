from typing import List, Optional
from yt_dlp import YoutubeDL

from models.track import Track


# Service to interact with YouTube using yt-dlp (Python lib)
# Fetches tracks from a YouTube playlist URL
# Searches for the first track matching a query
# Parses extracted info to create Track objects
# Handles errors gracefully, returning None or empty lists as needed
class YouTubeService:
    def __init__(self):
        self._base_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

    def get_tracks_from_playlist(self, playlist_url: str) -> List[Track]:
        ydl_opts = {
            **self._base_opts,
            "extract_flat": True,
            "noplaylist": False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)

            entries = info.get("entries") or []
            tracks: List[Track] = []

            for e in entries:
                if not isinstance(e, dict):
                    continue

                title = e.get("title")
                video_id = e.get("id")
                if not title or not video_id:
                    continue

                artist = e.get("artist") or e.get("uploader") or e.get("channel")

                tracks.append(
                    Track(
                        title=title,
                        artist=artist,
                        url=f"https://music.youtube.com/watch?v={video_id}",
                    )
                )

            return tracks

        except Exception:
            return []

    def search_first(self, query: str) -> Optional[Track]:
        ydl_opts = {
            **self._base_opts,
            "noplaylist": True,
            "default_search": "ytsearch1",
            "extract_flat": False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)

            entries = info.get("entries") if isinstance(info, dict) else None
            if not entries:
                return None

            data = entries[0]
            if not isinstance(data, dict):
                return None

            title = data.get("title")
            video_id = data.get("id")
            if not title or not video_id:
                return None

            artist = data.get("artist") or data.get("uploader") or data.get("channel")

            return Track(
                title=title,
                artist=artist,
                url=f"https://music.youtube.com/watch?v={video_id}",
            )

        except Exception:
            return None
