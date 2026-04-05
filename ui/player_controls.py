import customtkinter as ctk
from ui.theme import (
    BTN,
    HOVER,
    ACCENT,
    ACCENT_HOVER,
    TEXT,
    TEXT_MUTED,
    STROKE,
    FOOTER,
    TEXT_ON_ACCENT,
    CARD,
)


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
        on_seek=None,
    ):
        super().__init__(parent, height=120, corner_radius=0)

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
        self.grid_columnconfigure(1, weight=1)

        now_playing_frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14, border_width=1, border_color=STROKE)
        now_playing_frame.grid(row=0, column=0, padx=(14, 8), pady=10, sticky="nsew")

        self.now_playing_title = ctk.CTkLabel(
            now_playing_frame,
            text="Nenhuma música selecionada",
            text_color=TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
            width=250,
        )
        self.now_playing_title.pack(anchor="w", padx=12, pady=(10, 2))

        self.now_playing_subtitle = ctk.CTkLabel(
            now_playing_frame,
            text="Selecione uma faixa para começar",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=12),
            anchor="w",
            width=250,
        )
        self.now_playing_subtitle.pack(anchor="w", padx=12, pady=(0, 10))

        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=0, column=1, padx=8, pady=10, sticky="nsew")
        center_frame.grid_columnconfigure(0, weight=1)

        self.playback_seek_slider = ctk.CTkSlider(
            center_frame,
            from_=0,
            to=1,
            number_of_steps=1000,
            command=self._on_seek_slider_change,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            fg_color=BTN,
        )
        self.playback_seek_slider.grid(row=0, column=0, padx=4, sticky="ew")
        self.playback_seek_slider.set(0)

        time_row = ctk.CTkFrame(center_frame, fg_color="transparent")
        time_row.grid(row=1, column=0, sticky="ew", pady=(4, 12))
        time_row.grid_columnconfigure(1, weight=1)

        self.playback_time_label = ctk.CTkLabel(time_row, text="0:00 / 0:00", text_color=TEXT_MUTED)
        self.playback_time_label.grid(row=0, column=0, sticky="w")

        self.status_label = ctk.CTkLabel(
            time_row,
            text="Pronto",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=11),
        )
        self.status_label.grid(row=0, column=2, sticky="e")

        controls_row = ctk.CTkFrame(center_frame, fg_color="transparent")
        controls_row.grid(row=2, column=0, sticky="ew")

        self.shuffle_btn = ctk.CTkButton(
            controls_row,
            text="🔀",
            width=42,
            command=self.on_shuffle,
            fg_color=BTN,
            hover_color=HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE,
        )

        self.prev_btn = ctk.CTkButton(
            controls_row,
            text="⏮",
            width=44,
            command=self.on_prev,
            fg_color=BTN,
            hover_color=HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE,
        )

        self.play_pause_btn = ctk.CTkButton(
            controls_row,
            text="▶",
            width=56,
            command=self.on_play_pause,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=TEXT_ON_ACCENT,
            font=ctk.CTkFont(size=16, weight="bold"),
        )

        self.next_btn = ctk.CTkButton(
            controls_row,
            text="⏭",
            width=44,
            command=self.on_next,
            fg_color=BTN,
            hover_color=HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE,
        )

        self.loop_btn = ctk.CTkButton(
            controls_row,
            text="🔁",
            width=42,
            command=self.on_loop,
            fg_color=BTN,
            hover_color=HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE,
        )

        self.shuffle_btn.pack(side="left", padx=3)
        self.prev_btn.pack(side="left", padx=3)
        self.play_pause_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=3)
        self.loop_btn.pack(side="left", padx=3)

        volume_frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14, border_width=1, border_color=STROKE)
        volume_frame.grid(row=0, column=2, padx=(8, 14), pady=10, sticky="nsew")

        volume_label = ctk.CTkLabel(volume_frame, text="Volume", text_color=TEXT_MUTED, font=ctk.CTkFont(size=11))
        volume_label.pack(anchor="w", padx=12, pady=(10, 4))

        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            width=160,
            number_of_steps=100,
            command=self.on_volume_change,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            fg_color=BTN,
        )
        self.volume_slider.pack(padx=12, pady=(0, 8))

        self.volume_value_label = ctk.CTkLabel(volume_frame, text=f"{self.initial_volume}%", text_color=TEXT)
        self.volume_value_label.pack(anchor="e", padx=12, pady=(0, 10))

        self._is_user_seeking = False
        self._last_seek_ratio = 0.0

        self.playback_seek_slider.bind("<ButtonPress-1>", self._on_seek_start)
        self.playback_seek_slider.bind("<ButtonRelease-1>", self._on_seek_end)

    def set_playing(self, is_playing: bool):
        self.play_pause_btn.configure(text="⏸" if is_playing else "▶")
        self.status_label.configure(text="Reproduzindo" if is_playing else "Pausado")

    def set_track_info(self, title: str | None, artist: str | None = None):
        if not title:
            self.now_playing_title.configure(text="Nenhuma música selecionada")
            self.now_playing_subtitle.configure(text="Selecione uma faixa para começar")
            return

        self.now_playing_title.configure(text=title)
        self.now_playing_subtitle.configure(text=artist or "Artista desconhecido")

    def set_shuffle_active(self, active: bool):
        if active:
            self.shuffle_btn.configure(
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color=TEXT_ON_ACCENT,
                border_width=0,
            )
        else:
            self.shuffle_btn.configure(
                fg_color=self._default_shuffle_color,
                hover_color=HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE,
            )

    def set_loop_active(self, active: bool):
        if active:
            self.loop_btn.configure(
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color=TEXT_ON_ACCENT,
                border_width=0,
            )
        else:
            self.loop_btn.configure(
                fg_color=self._default_loop_color,
                hover_color=HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE,
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

    def set_volume_display(self, value: int):
        self.volume_value_label.configure(text=f"{int(value)}%")
