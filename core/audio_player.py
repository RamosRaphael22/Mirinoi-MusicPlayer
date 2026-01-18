import threading
import subprocess
import time
from enum import Enum
import vlc
from yt_dlp import YoutubeDL

class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"

# Audio player class
# Manages audio playback using VLC
# Supports play, pause, and stop functionalities
# Calls a callback function when playback finishes naturally
# Uses threading to handle playback in the background
# Monitors real VLC playback state to avoid false track endings
class AudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance("--no-video")
        self.player = self.instance.media_player_new()

        self.current_url = None
        self.state = PlayerState.STOPPED

        self._lock = threading.RLock()
        self._play_id = 0
        self._stop_requested = False
        self._paused_time_ms = 0

        self.on_finished = None

        self._volume = 20

        self._last_known_track_duration_ms = 0
        try:
            self.player.audio_set_volume(self._volume)
        except Exception:
            pass

        self._last_known_track_duration_ms = 0    

    def play(self, video_url: str):
        with self._lock:
            if self.state == PlayerState.PAUSED and self.current_url == video_url:
                self._stop_requested = False

                if self.player.get_state() == vlc.State.Paused:
                    self.player.pause()
                    self.state = PlayerState.PLAYING

                    if self._paused_time_ms > 0:
                        time.sleep(0.05)
                        try:
                            self.player.set_time(self._paused_time_ms)
                        except Exception:
                            pass
                    return

                self._play_id += 1
                local_id = self._play_id

                self._stop_requested = False
                self.current_url = video_url
                self.state = PlayerState.PLAYING

                threading.Thread(
                    target=self._play_thread,
                    args=(local_id, self._paused_time_ms),
                    daemon=True
                ).start()
                return

            if self.state == PlayerState.PLAYING:
                return

            self._play_id += 1
            local_id = self._play_id

            self._stop_requested = False
            self.current_url = video_url
            self.state = PlayerState.PLAYING
            self._paused_time_ms = 0

            self._last_known_track_duration_ms = 0

            threading.Thread(
                target=self._play_thread,
                args=(local_id, 0),
                daemon=True
            ).start()

    def _play_thread(self, play_id: int, resume_time_ms: int = 0):
        finished_naturally = False

        try:
            audio_url = self._get_audio_stream_url(self.current_url)

            media = self.instance.media_new(audio_url)
            self.player.set_media(media)
            self.player.play()

            try:
                self.player.audio_set_volume(self._volume)
            except Exception:
                pass

            timeout = time.time() + 5
            while time.time() < timeout:
                state = self.player.get_state()
                if state in (vlc.State.Playing, vlc.State.Paused):
                    break
                time.sleep(0.1)

            state = self.player.get_state()
            if state not in (vlc.State.Playing, vlc.State.Paused):
                with self._lock:
                    if play_id == self._play_id:
                        self.state = PlayerState.STOPPED
                return

            if resume_time_ms > 0:
                try:
                    time.sleep(0.05)
                    self.player.set_time(resume_time_ms)
                except Exception:
                    pass

            while True:
                with self._lock:
                    if play_id != self._play_id or self._stop_requested:
                        return

                state = self.player.get_state()

                if state == vlc.State.Paused:
                    with self._lock:
                        if play_id == self._play_id:
                            self.state = PlayerState.PAUSED
                    time.sleep(0.2)
                    continue

                if state == vlc.State.Playing:
                    with self._lock:
                        if play_id == self._play_id:
                            self.state = PlayerState.PLAYING

                if state in (vlc.State.Ended, vlc.State.Error):
                    break

                time.sleep(0.3)

            finished_naturally = not self._stop_requested

        except Exception:
            finished_naturally = False

        finally:
            with self._lock:
                if play_id != self._play_id:
                    return

                self.state = PlayerState.STOPPED
                self._paused_time_ms = 0

            if finished_naturally and self.on_finished:
                self.on_finished()

    def pause(self):
        with self._lock:
            if self.state != PlayerState.PLAYING:
                return

            try:
                current_time = self.player.get_time()
                if current_time is not None and current_time > 0:
                    self._paused_time_ms = int(current_time)
            except Exception:
                self._paused_time_ms = 0

            self.player.pause()
            self.state = PlayerState.PAUSED

    def stop(self):
        with self._lock:
            self._stop_requested = True
            self._play_id += 1
            self.player.stop()
            self.state = PlayerState.STOPPED
            self._paused_time_ms = 0
            self._last_known_track_duration_ms = 0

    def _get_audio_stream_url(self, video_url: str) -> str:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "skip_download": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        direct = info.get("url")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()

        formats = info.get("formats") or []
        if not formats:
            raise RuntimeError("yt_dlp: no formats available")

        audio_formats = [f for f in formats if f.get("acodec") not in (None, "none")]
        best = audio_formats[-1] if audio_formats else formats[-1]

        u = best.get("url")
        if not u:
            raise RuntimeError("yt_dlp: could not extract stream url")

        return str(u).strip()

    def set_volume(self, volume: int):
        v = max(0, min(100, int(volume)))
        with self._lock:
            self._volume = v
            try:
                self.player.audio_set_volume(v)
            except Exception:
                pass

    def get_volume(self) -> int:
        with self._lock:
            try:
                v = self.player.audio_get_volume()
                if isinstance(v, int) and 0 <= v <= 100:
                    self._volume = v
            except Exception:
                pass
            return self._volume
            
    def get_current_playback_time_ms(self) -> int:
        with self._lock:
            try:
                current_time = self.player.get_time()
                return int(current_time) if current_time and current_time > 0 else 0
            except Exception:
                return 0

    def get_track_duration_ms(self) -> int:
        with self._lock:
            try:
                duration = self.player.get_length()
                duration_ms = int(duration) if duration and duration > 0 else 0

                if duration_ms > 0:
                    self._last_known_track_duration_ms = duration_ms

                return self._last_known_track_duration_ms
            except Exception:
                return self._last_known_track_duration_ms

    def get_playback_progress_ratio(self) -> float:
        track_duration_ms = self.get_track_duration_ms()
        if track_duration_ms <= 0:
            return 0.0

        current_time_ms = self.get_current_playback_time_ms()
        progress_ratio = current_time_ms / track_duration_ms

        if progress_ratio < 0:
            return 0.0
        if progress_ratio > 1:
            return 1.0
        return progress_ratio
    
    def seek_to_time_ms(self, target_time_ms: int):
        with self._lock:
            if self.state not in (PlayerState.PLAYING, PlayerState.PAUSED):
                return

            try:
                duration_ms = self.player.get_length()
                if duration_ms is not None and duration_ms > 0:
                    clamped = max(0, min(int(target_time_ms), int(duration_ms)))
                else:
                    clamped = max(0, int(target_time_ms))

                self.player.set_time(clamped)
            except Exception:
                pass


    def seek_to_progress_ratio(self, progress_ratio: float):
        progress_ratio = max(0.0, min(1.0, float(progress_ratio)))

        with self._lock:
            if self.state not in (PlayerState.PLAYING, PlayerState.PAUSED):
                return

            try:
                duration_ms = self.player.get_length()
                if duration_ms is None or duration_ms <= 0:
                    return

                target_time_ms = int(duration_ms * progress_ratio)
                self.player.set_time(target_time_ms)
            except Exception:
                pass
