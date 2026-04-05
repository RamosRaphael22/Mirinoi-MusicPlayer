import customtkinter as ctk
from ui.theme import BTN, HOVER, ACCENT, ACCENT_HOVER, TEXT, TEXT_MUTED, STROKE, FOOTER, TEXT_ON_ACCENT


class PlayerControls(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_play_pause=None,
        on_next=None,
        on_prev=None,
        on_shuffle=None,
        on_loop=None,
        on_volume_change=None,
        initial_volume=20,
        on_seek=None
    ):
        super().__init__(parent, height=104)

        self.configure(fg_color=FOOTER)

        self.on_play_pause = on_play_pause
        self.on_next = on_next
        self.on_prev = on_prev
        self.on_shuffle = on_shuffle
        self.on_loop = on_loop
        self.on_volume_change = on_volume_change
        self.on_seek = on_seek

        self.initial_volume = initial_volume

        self._default_shuffle_color = BTN
        self._default_loop_color = BTN

        self._build_ui()

        self.volume_slider.set(self.initial_volume)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.now_playing_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.now_playing_frame.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=10)

        self.now_playing_title = ctk.CTkLabel(
            self.now_playing_frame,
            text="Nenhuma música tocando",
            text_color=TEXT,
            font=ctk.CTkFont(size=19, weight="bold")
        )
        self.now_playing_title.pack(anchor="w")

        self.now_playing_artist = ctk.CTkLabel(
            self.now_playing_frame,
            text="",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=14)
        )
        self.now_playing_artist.pack(anchor="w", pady=(2, 0))

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=1, sticky="nsew")

        self.seek_row = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.seek_row.pack(anchor="center", pady=(8, 4))

        self.buttons_row = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.buttons_row.pack(anchor="center", pady=(2, 8))

        self.prev_btn = ctk.CTkButton(self.buttons_row, text="⏮", command=self.on_prev,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.play_pause_btn = ctk.CTkButton(self.buttons_row, text="▶", command=self.on_play_pause,
                                            fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                            text_color="white")


        self.next_btn = ctk.CTkButton(self.buttons_row, text="⏭", command=self.on_next,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.shuffle_btn = ctk.CTkButton(self.buttons_row, text="🔀", command=self.on_shuffle,
                                        fg_color=BTN, hover_color=HOVER,
                                        text_color=TEXT, border_width=1, border_color=STROKE)

        self.loop_btn = ctk.CTkButton(self.buttons_row, text="🔁", command=self.on_loop,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.volume_section = ctk.CTkFrame(self, fg_color="transparent")
        self.volume_section.grid(row=0, column=2, sticky="e", padx=(8, 16), pady=10)

        self.volume_label = ctk.CTkLabel(self.volume_section, text="Volume", text_color=TEXT_MUTED)
        self.volume_label.pack(anchor="e", pady=(0, 4))

        self.volume_slider = ctk.CTkSlider(self.volume_section, from_=0, to=100, width=220,number_of_steps=100, command=self.on_volume_change)
        self.volume_slider.pack(anchor="e")

        self.playback_seek_slider = ctk.CTkSlider(
            self.seek_row,
            from_=0,
            to=1,
            width=560,
            number_of_steps=1000,
            command=self._on_seek_slider_change
        )
        self.playback_seek_slider.set(0)

        self._is_user_seeking = False
        self._last_seek_ratio = 0.0

        self.playback_seek_slider.bind("<ButtonPress-1>", self._on_seek_start)
        self.playback_seek_slider.bind("<ButtonRelease-1>", self._on_seek_end)

        self.playback_time_label = ctk.CTkLabel(self.seek_row, text="0:00 / 0:00", text_color=TEXT_MUTED)

        self.playback_seek_slider.pack(side="left", padx=(0, 8))
        self.playback_time_label.pack(side="left")

        self.shuffle_btn.pack(side="left", padx=5)
        self.prev_btn.pack(side="left", padx=5)
        self.play_pause_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.loop_btn.pack(side="left", padx=5)

    def set_track_info(self, title: str | None, artist: str | None):
        if not title:
            self.now_playing_title.configure(text="Nenhuma música tocando")
            self.now_playing_artist.configure(text="")
            return

        self.now_playing_title.configure(text=title)
        self.now_playing_artist.configure(text=artist or "Artista desconhecido")

    def set_playing(self, is_playing: bool):
        self.play_pause_btn.configure(text="⏸" if is_playing else "▶")

    def set_shuffle_active(self, active: bool):
        if active:
            self.shuffle_btn.configure(
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color=TEXT_ON_ACCENT,
                border_width=0
            )
        else:
            self.shuffle_btn.configure(
                fg_color=self._default_shuffle_color,
                hover_color=HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE
            )

    def set_loop_active(self, active: bool):
        if active:
            self.loop_btn.configure(
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color=TEXT_ON_ACCENT,
                border_width=0
            )
        else:
            self.loop_btn.configure(
                fg_color=self._default_loop_color,
                hover_color=HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE
            )

    def update_playback_progress(self, progress_ratio: float, current_time_ms: int, track_duration_ms: int):
        progress_ratio = max(0.0, min(1.0, float(progress_ratio)))

        if not self._is_user_seeking:
            self.playback_seek_slider.set(progress_ratio)

        formatted_current = self._format_milliseconds_to_time(current_time_ms)
        formatted_total = self._format_milliseconds_to_time(track_duration_ms)
        self.playback_time_label.configure(text=f"{formatted_current} / {formatted_total}")

    def _format_milliseconds_to_time(self, milliseconds: int) -> str:
        total_seconds = max(0, int(milliseconds) // 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    def _on_seek_start(self, _event):
        self._is_user_seeking = True

    def _on_seek_end(self, _event):
        self._is_user_seeking = False
        if self.on_seek is not None:
            self.on_seek(self._last_seek_ratio)

    def _on_seek_slider_change(self, value):
        ratio = max(0.0, min(1.0, float(value)))
        self._last_seek_ratio = ratio
