import customtkinter as ctk
import threading

from core.csv_service import CSVService
from core.yt_service import YouTubeService
from core.audio_player import AudioPlayer
from core.queue_manager import QueueManager

from ui.playlist_sidebar import PlaylistSidebar
from ui.track_list import TrackList
from ui.player_controls import PlayerControls


class MainWindow(ctk.CTk):
    # ───────────────────────────────
    # Estados do player
    # ───────────────────────────────
    STOPPED = "STOPPED"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"

    def __init__(self):
        super().__init__()

        # 🔹 Estado
        self.player_state = self.STOPPED
        self.shuffle_enabled = False

        # 🔹 Janela
        self.title("Mirinoi Player")
        self.geometry("900x600")

        # 🔹 Serviços
        self.csv_service = CSVService("playlists.csv")
        self.yt_service = YouTubeService()
        self.audio_player = AudioPlayer()
        self.queue_manager = QueueManager()

        # 🔹 Autoplay
        self.audio_player.on_finished = self._on_track_finished

        # 🔹 UI
        self._build_layout()

    # ───────────────────────────────
    # Layout
    # ───────────────────────────────
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = PlaylistSidebar(
            self,
            csv_service=self.csv_service,
            on_select_callback=self._on_playlist_selected
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.track_list = TrackList(
            self,
            on_track_selected=self._on_track_selected
        )
        self.track_list.grid(row=0, column=1, sticky="nsew")

        self.controls = PlayerControls(
            self,
            on_play=self._play_current,
            on_pause=self._pause,
            on_next=self._play_next,
            on_prev=self._play_prev,
            on_shuffle=self._toggle_shuffle
        )
        self.controls.grid(row=1, column=0, columnspan=2, sticky="ew")

    # ───────────────────────────────
    # Playlist
    # ───────────────────────────────
    def _on_playlist_selected(self, playlist):
        self._stop_player()

        self.track_list.load_tracks([])
        self.queue_manager.set_queue([])

        threading.Thread(
            target=self._load_tracks_thread,
            args=(playlist.url,),
            daemon=True
        ).start()

    def _load_tracks_thread(self, url):
        tracks = self.yt_service.get_tracks_from_playlist(url)
        self.after(0, lambda: self._update_tracks(tracks))

    def _update_tracks(self, tracks):
        self.queue_manager.set_queue(tracks)
        self.track_list.load_tracks(tracks)

        self.player_state = self.STOPPED

    # ───────────────────────────────
    # Track selection
    # ───────────────────────────────
    def _on_track_selected(self, track):
        self.queue_manager.current_index = self.track_list.selected_index
        self._force_play_current()

    # ───────────────────────────────
    # Player core
    # ───────────────────────────────
    def _play_current(self):
        # Play NÃO troca música se já estiver tocando
        if self.player_state == self.PLAYING:
            return

        if self.player_state in (self.STOPPED, self.PAUSED):
            self._force_play_current()

    def _force_play_current(self):
        track = self.queue_manager.current()
        index = self.queue_manager.current_index

        if not track:
            return

        self.audio_player.stop()
        self.audio_player.play(track.url)

        self.track_list.set_highlight(index)
        self.player_state = self.PLAYING

    def _pause(self):
        if self.player_state != self.PLAYING:
            return

        self.audio_player.stop()
        self.player_state = self.PAUSED

    def _stop_player(self):
        self.audio_player.stop()
        self.player_state = self.STOPPED

    # ───────────────────────────────
    # Navigation
    # ───────────────────────────────
    def _play_next(self):
        track = self.queue_manager.next()
        if not track:
            return

        self._force_play_current()

    def _play_prev(self):
        track = self.queue_manager.prev()
        if not track:
            return

        self._force_play_current()

    # ───────────────────────────────
    # Autoplay
    # ───────────────────────────────
    def _on_track_finished(self):
        # Autoplay SOMENTE se estava tocando
        if self.player_state != self.PLAYING:
            return

        self.after(0, self._play_next)

    # ───────────────────────────────
    # Shuffle
    # ───────────────────────────────
    def _toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled

        if self.shuffle_enabled:
            self.queue_manager.shuffle()
        else:
            self.queue_manager.unshuffle()

        self.track_list.load_tracks(self.queue_manager.queue)
        self.track_list.set_highlight(self.queue_manager.current_index)
        self.controls.set_shuffle_active(self.shuffle_enabled)
