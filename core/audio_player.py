import subprocess
import threading
from enum import Enum

# Audio player status
class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"

# Audio player class
# Manages audio playback using ffplay and yt-dlp
# Supports play, pause, and stop functionalities
# Calls a callback function when playback finishes naturally
# Usage of threading to handle playback in the background
class AudioPlayer:
    def __init__(self):
        self.ffplay_process = None
        self.current_url = None
        self.state = PlayerState.STOPPED

        self._lock = threading.RLock()
        self._play_id = 0
        self._stop_requested = False

        self.on_finished = None

    # Play audio from a video URL
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

    # Reproduction thread
    def _play_thread(self, play_id: int):
        try:
            audio_url = self._get_audio_stream_url(self.current_url)

            with self._lock:
                if play_id != self._play_id:
                    return

                self.ffplay_process = subprocess.Popen(
                    [
                       "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        audio_url
                    ],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            self.ffplay_process.wait()
            finished_naturally = not self._stop_requested

        except Exception:
            finished_naturally = False

        finally:
            with self._lock:
                if play_id != self._play_id:
                    return

                self.ffplay_process = None
                self.state = PlayerState.STOPPED

            if finished_naturally and self.on_finished:
                self.on_finished()

    def pause(self):
        with self._lock:
            if self.state != PlayerState.PLAYING:
                return

            self._stop_requested = True
            self._terminate_process()
            self.state = PlayerState.PAUSED

    def stop(self):
        with self._lock:
            self._stop_requested = True
            self._play_id += 1
            self._terminate_process()
            self.state = PlayerState.STOPPED

    def _terminate_process(self):
        if self.ffplay_process:
            try:
                self.ffplay_process.kill()
            except Exception:
                pass
            self.ffplay_process = None

    def _get_audio_stream_url(self, video_url: str) -> str:
        result = subprocess.check_output(
            ["yt-dlp", "-f", "bestaudio", "-g", video_url],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip().split("\n")[0]
