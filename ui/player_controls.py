import customtkinter as ctk


class PlayerControls(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_play=None,
        on_pause=None,
        on_next=None,
        on_prev=None,
        on_shuffle=None,
    ):
        super().__init__(parent, height=80)

        self.on_play = on_play
        self.on_pause = on_pause
        self.on_next = on_next
        self.on_prev = on_prev
        self.on_shuffle = on_shuffle

        self._build_ui()


    # 🔹 UI
    def _build_ui(self):
        self.play_btn = ctk.CTkButton(self, text="▶", command=self.on_play)
        self.pause_btn = ctk.CTkButton(self, text="⏸", command=self.on_pause)
        self.prev_btn = ctk.CTkButton(self, text="⏮", command=self.on_prev)
        self.next_btn = ctk.CTkButton(self, text="⏭", command=self.on_next)

        self.shuffle_btn = ctk.CTkButton(
            self,
            text="🔀",
            command=self.on_shuffle,
            width=40,
            fg_color="transparent")

        self.prev_btn.pack(side="left", padx=5)
        self.play_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.shuffle_btn.pack(side="left", padx=5)
    
    def set_shuffle_active(self, active: bool):
        if active:
            self.shuffle_btn.configure(fg_color="#2ecc71")
        else:
            self.shuffle_btn.configure(fg_color="transparent")




