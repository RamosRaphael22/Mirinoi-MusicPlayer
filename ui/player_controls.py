import customtkinter as ctk

# Player control buttons: play, pause, next, previous, shuffle
# Calls provided callbacks on button presses
# Allows visual indication of shuffle state
class PlayerControls(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_play=None,
        on_pause=None,
        on_next=None,
        on_prev=None,
        on_shuffle=None,
        on_loop=None
    ):
        super().__init__(parent, height=80)

        self.on_play = on_play
        self.on_pause = on_pause
        self.on_next = on_next
        self.on_prev = on_prev
        self.on_shuffle = on_shuffle
        self.on_loop = on_loop

        self._default_shuffle_color = "#db03fc"
        self._default_loop_color = "#db03fc"

        self._build_ui()

    def _build_ui(self):
        self.play_btn = ctk.CTkButton(self, text="▶", command=self.on_play, fg_color="#db03fc", hover_color="#bb16ca")
        self.pause_btn = ctk.CTkButton(self, text="⏸", command=self.on_pause, fg_color="#db03fc", hover_color="#bb16ca")
        self.prev_btn = ctk.CTkButton(self, text="⏮", command=self.on_prev, fg_color="#db03fc", hover_color="#bb16ca")
        self.next_btn = ctk.CTkButton(self, text="⏭", command=self.on_next, fg_color="#db03fc", hover_color="#bb16ca")

        self.shuffle_btn = ctk.CTkButton(
            self,
            text="🔀",
            command=self.on_shuffle,
            fg_color=self._default_shuffle_color,
            hover_color="#bb16ca"
            )
        self.loop_btn = ctk.CTkButton(self, text="🔁", command=self.on_loop, fg_color="#db03fc", hover_color="#bb16ca")

        self.prev_btn.pack(side="left", padx=5)
        self.play_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.shuffle_btn.pack(side="left", padx=5)
        self.loop_btn.pack(side="left", padx=5)

    def set_shuffle_active(self, active: bool):
        if active:
            self.shuffle_btn.configure(fg_color="#bb16ca")
        else:
            self.shuffle_btn.configure(fg_color=self._default_shuffle_color)

    def set_loop_active(self, active: bool):
        if active:
            self.loop_btn.configure(fg_color="#bb16ca")
        else:
            self.loop_btn.configure(fg_color=self._default_shuffle_color)