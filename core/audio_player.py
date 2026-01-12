import subprocess
import threading
import time


class AudioPlayer:
    def __init__(self):
        self.ffplay_process = None
        self.current_url = None
        self.is_playing = False

    # 🔹 Tocar música
    def play(self, video_url: str):
        self.stop()
        self.current_url = video_url

        threading.Thread(
            target=self._play_thread,
            daemon=True
        ).start()

    # 🔹 Thread de execução
    def _play_thread(self):
        try:
            audio_url = self._get_audio_stream_url(self.current_url)

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

            self.is_playing = True
            self.ffplay_process.wait()

        finally:
            self.is_playing = False
            self.ffplay_process = None

    # 🔹 Gera URL direta do áudio
    def _get_audio_stream_url(self, video_url: str) -> str:
        result = subprocess.check_output(
            [
                "yt-dlp",
                "-f",
                "bestaudio",
                "-g",
                video_url
            ],
            stderr=subprocess.DEVNULL,
            text=True
        )

        return result.strip().split("\n")[0]

    # 🔹 Para a reprodução
    def stop(self):
        if self.ffplay_process:
            self.ffplay_process.kill()
            self.ffplay_process = None
            self.is_playing = False

    # 🔹 Pause (simulado)
    def pause(self):
        self.stop()