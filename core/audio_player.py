import threading
import subprocess
import time
from enum import Enum
import vlc


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

        self.on_finished = None

    def play(self, video_url: str):
        with self._lock:
            if self.state == PlayerState.PLAYING:
                return

            self._play_id += 1
            local_id = self._play_id

            self._stop_requested = False
            self.current_url = video_url
            self.state = PlayerState.PLAYING

            threading.Thread(
                target=self._play_thread,
                args=(local_id,),
                daemon=True
            ).start()

    def _play_thread(self, play_id: int):
        finished_naturally = False
        
        try:
            audio_url = self._get_audio_stream_url(self.current_url)

            media = self.instance.media_new(audio_url)
            self.player.set_media(media)
            self.player.play()

            timeout = time.time() + 5
            while time.time() < timeout:
                if self.player.get_state() == vlc.State.Playing:
                    break
                time.sleep(0.1)

            if self.player.get_state() != vlc.State.Playing:
                with self._lock:
                    self.state = PlayerState.STOPPED
                return

            while True:
                with self._lock:
                    if play_id != self._play_id or self._stop_requested:
                        return

                state = self.player.get_state()
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

            if finished_naturally and self.on_finished:
                self.on_finished()

    def pause(self):
        with self._lock:
            if self.state != PlayerState.PLAYING:
                return

            self._stop_requested = True
            self.player.stop()
            self.state = PlayerState.PAUSED

    def stop(self):
        with self._lock:
            self._stop_requested = True
            self._play_id += 1
            self.player.stop()
            self.state = PlayerState.STOPPED

    def _get_audio_stream_url(self, video_url: str) -> str:
        result = subprocess.check_output(
            ["yt-dlp", "-f", "bestaudio", "-g", video_url],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip().split("\n")[0]
