import customtkinter as ctk

class PlayerControls(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_play_pause=None,
        on_next=None,
        on_prev=None,
        on_shuffle=None,
        on_loop=None
    ):
        super().__init__(parent, height=80)

        self.on_play_pause = on_play_pause
        self.on_next = on_next
        self.on_prev = on_prev
        self.on_shuffle = on_shuffle
        self.on_loop = on_loop

        self._default_shuffle_color = "#db03fc"
        self._default_loop_color = "#db03fc"

        self._build_ui()

    def _build_ui(self):
        self.prev_btn = ctk.CTkButton(self, text="⏮", command=self.on_prev,
                                      fg_color="#db03fc", hover_color="#bb16ca")

        self.play_pause_btn = ctk.CTkButton(self, text="▶",
                                            command=self.on_play_pause,
                                            fg_color="#db03fc",
                                            hover_color="#bb16ca")

        self.next_btn = ctk.CTkButton(self, text="⏭", command=self.on_next,
                                      fg_color="#db03fc", hover_color="#bb16ca")

        self.shuffle_btn = ctk.CTkButton(
            self,
            text="🔀",
            command=self.on_shuffle,
            fg_color=self._default_shuffle_color,
            hover_color="#bb16ca"
        )

        self.loop_btn = ctk.CTkButton(
            self,
            text="🔁",
            command=self.on_loop,
            fg_color=self._default_loop_color,
            hover_color="#bb16ca"
        )

        self.prev_btn.pack(side="left", padx=5)
        self.play_pause_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.shuffle_btn.pack(side="left", padx=5)
        self.loop_btn.pack(side="left", padx=5)

    def set_playing(self, is_playing: bool):
        self.play_pause_btn.configure(text="⏸" if is_playing else "▶")

    def set_shuffle_active(self, active: bool):
        self.shuffle_btn.configure(
            fg_color="#bb16ca" if active else self._default_shuffle_color
        )

    def set_loop_active(self, active: bool):
        self.loop_btn.configure(
            fg_color="#bb16ca" if active else self._default_loop_color
        )
