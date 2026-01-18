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
        super().__init__(parent, height=80)

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
        self.prev_btn = ctk.CTkButton(self, text="⏮", command=self.on_prev,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.play_pause_btn = ctk.CTkButton(self, text="▶", command=self.on_play_pause,
                                            fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                            text_color="white")


        self.next_btn = ctk.CTkButton(self, text="⏭", command=self.on_next,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.shuffle_btn = ctk.CTkButton(self, text="🔀", command=self.on_shuffle,
                                        fg_color=BTN, hover_color=HOVER,
                                        text_color=TEXT, border_width=1, border_color=STROKE)

        self.loop_btn = ctk.CTkButton(self, text="🔁", command=self.on_loop,
                                    fg_color=BTN, hover_color=HOVER,
                                    text_color=TEXT, border_width=1, border_color=STROKE)

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, width=150,number_of_steps=100, command=self.on_volume_change)

        self.playback_seek_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=1,
            width=400,
            number_of_steps=1000,
            command=self._on_seek_slider_change
        )
        self.playback_seek_slider.set(0)

        self._is_user_seeking = False
        self._last_seek_ratio = 0.0

        self.playback_seek_slider.bind("<ButtonPress-1>", self._on_seek_start)
        self.playback_seek_slider.bind("<ButtonRelease-1>", self._on_seek_end)

        self.playback_time_label = ctk.CTkLabel(self, text="0:00 / 0:00", text_color=TEXT_MUTED)

        self.prev_btn.pack(side="left", padx=5, pady=10)
        self.play_pause_btn.pack(side="left", padx=5, pady=10)
        self.next_btn.pack(side="left", padx=5, pady=10)
        self.shuffle_btn.pack(side="left", padx=5, pady=10)
        self.loop_btn.pack(side="left", padx=5, pady=10)
        self.playback_seek_slider.pack(side="left", padx=(10, 5))
        self.playback_time_label.pack(side="left", padx=(8, 15))
        self.volume_slider.pack(side="left", padx=(10, 15))

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

