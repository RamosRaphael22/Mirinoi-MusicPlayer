import customtkinter as ctk
import threading

from core.csv_service import CSVService
from core.yt_service import YouTubeService
from core.audio_player import AudioPlayer, PlayerState
from core.queue_manager import QueueManager

from ui.playlist_sidebar import PlaylistSidebar
from ui.track_list import TrackList
from ui.player_controls import PlayerControls

# Main application window
# Integrates playlist sidebar, track list, and player controls
# Manages state of audio player and track queue
# Handles user interactions for playing, pausing, navigating tracks, and shuffling
# Uses threading to load tracks without blocking the UI
# Responds to track completion events to autoplay next track
# Coordinates between CSV service, YouTube service, audio player, and queue manager
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.shuffle_enabled = False
        self.loop_enabled = False

        self.title("Mirinoi Player")
        self.geometry("900x600")

        self.csv_service = CSVService("playlists.csv")
        self.yt_service = YouTubeService()
        self.audio_player = AudioPlayer()
        self.queue_manager = QueueManager()

        self.audio_player.on_finished = self._on_track_finished

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_layout()

        self._playback_progress_update_job = None
        self._schedule_playback_progress_updates()

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = PlaylistSidebar(
            self,
            csv_service=self.csv_service,
            on_select_callback=self._on_playlist_selected,
            on_remove_callback=self._on_playlist_removed
        )

        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.track_list = TrackList(
            self,
            on_track_selected=self._on_track_selected
        )
        self.track_list.grid(row=0, column=1, sticky="nsew")

        self.controls = PlayerControls(
            self,
            on_play_pause=self._on_play_pause,
            on_next=self._play_next,
            on_prev=self._play_prev,
            on_shuffle=self._toggle_shuffle,
            on_loop=self._toggle_loop,
            on_volume_change=self._on_volume_change,
            initial_volume=self.audio_player.get_volume()
        )

        self.controls.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _on_playlist_selected(self, playlist):
        self._stop_player()

        self.track_list.show_loading()
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

    def _on_track_selected(self, track):
        self.queue_manager.current_index = self.track_list.selected_index
        self._force_play_current()

    def _play_current(self):
        track = self.queue_manager.current()
        if not track:
            return

        self.audio_player.play(track.url)
        self.controls.set_playing(self.audio_player.state == PlayerState.PLAYING)

    def _force_play_current(self):
        track = self.queue_manager.current()
        index = self.queue_manager.current_index

        if not track:
            return

        self.audio_player.stop()
        self.audio_player.play(track.url)

        self.track_list.set_highlight(index)
        self.controls.set_playing(True)

    def _pause(self):
        self.audio_player.pause()
        self.controls.set_playing(False)

    def _stop_player(self):
        self.audio_player.stop()
        self.controls.update_playback_progress(0.0, 0, 0)
        self.controls.set_playing(False)

    def _play_next(self):
        track = self.queue_manager.next()

        if not track:
            if self.loop_enabled and self.queue_manager.queue:
                self.queue_manager.current_index = 0
                self._force_play_current()
            else:
                self._stop_player()
            return

        self._force_play_current()

    def _play_prev(self):
        track = self.queue_manager.prev()
        if not track:
            return

        self._force_play_current()

    def _on_track_finished(self):
        if self.audio_player.state != PlayerState.STOPPED:
            return

        self.after(0, self._play_next)

    def _toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled

        if self.shuffle_enabled:
            self.queue_manager.shuffle()
        else:
            self.queue_manager.unshuffle()

        self.track_list.load_tracks(self.queue_manager.queue)
        self.track_list.set_highlight(self.queue_manager.current_index)
        self.controls.set_shuffle_active(self.shuffle_enabled)

    def _on_playlist_removed(self, playlist_id):
        self._stop_player()
        self.queue_manager.set_queue([])
        self.track_list.load_tracks([])

    def _on_close(self):
        if self._playback_progress_update_job is not None:
            try:
                self.after_cancel(self._playback_progress_update_job)
            except Exception:
                pass

        self._stop_player()
        self.destroy()

    def _toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        self.controls.set_loop_active(self.loop_enabled)

    def _on_play_pause(self):
        state = self.audio_player.state

        if state == PlayerState.PLAYING:
            self.audio_player.pause()
            self.controls.set_playing(False)
            return

        track = self.queue_manager.current()
        if not track:
            return

        self.audio_player.play(track.url)
        self.controls.set_playing(True)

    def _on_volume_change(self, value):
        self.audio_player.set_volume(int(value))

    def _schedule_playback_progress_updates(self):
        self._update_playback_progress_ui()


    def _update_playback_progress_ui(self):
        if self.audio_player.state in (PlayerState.PLAYING, PlayerState.PAUSED):
            current_time_ms = self.audio_player.get_current_playback_time_ms()
            track_duration_ms = self.audio_player.get_track_duration_ms()
            progress_ratio = self.audio_player.get_playback_progress_ratio()

            self.controls.update_playback_progress(
                progress_ratio=progress_ratio,
                current_time_ms=current_time_ms,
                track_duration_ms=track_duration_ms
            )
        else:
            self.controls.update_playback_progress(
                progress_ratio=0.0,
                current_time_ms=0,
                track_duration_ms=0
            )

        self._playback_progress_update_job = self.after(200, self._update_playback_progress_ui)

