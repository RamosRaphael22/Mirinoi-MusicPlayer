import customtkinter as ctk
import threading
from tkinter import messagebox

from core.csv_service import CSVService
from core.yt_service import YouTubeService
from core.audio_player import AudioPlayer
from core.queue_manager import QueueManager

from ui.playlist_sidebar import PlaylistSidebar
from ui.track_list import TrackList
from ui.player_controls import PlayerControls


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 🔹 Estado
        self.shuffle_enabled = False

        # 🔹 Janela
        self.title("Mirinoi Player")
        self.geometry("900x600")

        # 🔹 Serviços (backend)
        self.csv_service = CSVService("playlists.csv")
        self.yt_service = YouTubeService()
        self.audio_player = AudioPlayer()
        self.queue_manager = QueueManager()

        # 🔹 UI (depois dos serviços)
        self._build_layout()

    # 🔹 Layout
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = PlaylistSidebar(
            self,
            csv_service=self.csv_service,
            on_select_callback=self._on_playlist_selected
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Lista de músicas
        self.track_list = TrackList(
            self,
            on_track_selected=self._on_track_selected
        )
        self.track_list.grid(row=0, column=1, sticky="nsew")

        # Controles
        self.controls = PlayerControls(
            self,
            on_play=self._play_current,
            on_pause=self._pause,
            on_next=self._play_next,
            on_prev=self._play_prev,
            on_shuffle=self._toggle_shuffle
        )
        self.controls.grid(row=1, column=0, columnspan=2, sticky="ew")

    # 🔹 Playlist selecionada
    def _on_playlist_selected(self, playlist):
        """Agora acessa atributos do objeto Playlist"""
        self.track_list.load_tracks([])
        threading.Thread(
            target=self._load_tracks_thread,
            args=(playlist.url,),  # ✅ atributo do objeto
            daemon=True
        ).start()

    def _load_tracks_thread(self, url):
        tracks = self.yt_service.get_tracks_from_playlist(url)
        self.after(0, lambda: self._update_tracks(tracks))

    def _update_tracks(self, tracks):
        # 🔹 tracks agora são objetos Track
        self.track_list.load_tracks(tracks)
        self.queue_manager.set_queue(tracks)

    # 🔹 Música selecionada
    def _on_track_selected(self, track):
        index = self.track_list.selected_index
        self.queue_manager.current_index = index
        self._play_current()

    # 🔹 Player actions
    def _play_current(self):
        track = self.queue_manager.current()
        if track:
            self.audio_player.play(track.url)

    def _pause(self):
        self.audio_player.pause()

    def _play_next(self):
        track = self.queue_manager.next()
        if track:
            self.audio_player.play(track.url)

    def _play_prev(self):
        track = self.queue_manager.prev()
        if track:
            self.audio_player.play(track.url)

    # 🔹 Shuffle
    def _toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        if self.shuffle_enabled:
            self.queue_manager.shuffle()
        else:
            self.queue_manager.unshuffle()

        # 🔹 Atualiza lista e botão
        self.track_list.load_tracks(self.queue_manager.queue)
        self.controls.set_shuffle_active(self.shuffle_enabled)
