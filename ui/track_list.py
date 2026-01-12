import customtkinter as ctk

class TrackList(ctk.CTkFrame):
    def __init__(self, parent, on_track_selected=None):
        super().__init__(parent)
        self.on_track_selected = on_track_selected

        self.tracks = []          # 🔹 lista de objetos Track
        self.selected_index = None
        self.track_buttons = []

        self._build_ui()

    # 🔹 UI
    def _build_ui(self):
        self.title = ctk.CTkLabel(
            self,
            text="Músicas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title.pack(pady=10)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)

    # 🔹 Carrega músicas na lista
    def load_tracks(self, tracks):
        self.tracks = tracks
        self.selected_index = None

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.track_buttons.clear()

        for index, track in enumerate(tracks):
            btn = ctk.CTkButton(
                self.scroll,
                text=f"{index + 1}. {track.title}",  # 🔹 Track tem atributo .title
                anchor="w",
                command=lambda i=index: self._select_track(i)
            )
            btn.pack(fill="x", pady=2)
            self.track_buttons.append(btn)

    # 🔹 Seleção de música
    def _select_track(self, index):
        self.selected_index = index

        for i, btn in enumerate(self.track_buttons):
            btn.configure(fg_color="#1f6aa5" if i == index else None)

        if self.on_track_selected:
            self.on_track_selected(self.tracks[index])  # 🔹 passa objeto Track