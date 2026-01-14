import customtkinter as ctk

# UI component to display and manage the list of tracks
# Allows track selection and highlights the selected track
# Calls a callback when a track is selected
# Provides method to load tracks into the list
# Allows setting highlight on a specific track
class TrackList(ctk.CTkFrame):
    def __init__(self, parent, on_track_selected=None):
        super().__init__(parent)

        self.on_track_selected = on_track_selected

        self.tracks = []
        self.selected_index = None
        self.track_buttons = []

        self.default_fg_color = None

        self._build_ui()

    def _build_ui(self):
        self.title = ctk.CTkLabel(
            self,
            text="Músicas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title.pack(pady=10)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)

    def load_tracks(self, tracks):
        self.tracks = tracks
        self.selected_index = None

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.track_buttons.clear()
        self.default_fg_color = None

        for index, track in enumerate(tracks):
            text = (
                f"{index + 1}. {track.title} - {track.artist}"
                if track.artist
                else f"{index + 1}. {track.title}"
            )

            btn = ctk.CTkButton(
                self.scroll,
                text=text,
                anchor="w",
                command=lambda i=index: self._select_track(i)
            )

            if self.default_fg_color is None:
                self.default_fg_color = btn.cget("fg_color")

            btn.pack(fill="x", pady=2)
            self.track_buttons.append(btn)

    def _select_track(self, index):
        self.selected_index = index
        self.set_highlight(index)

        if self.on_track_selected:
            self.on_track_selected(self.tracks[index])

    def set_highlight(self, index):
        self.highlighted_index = index
        self.selected_index = index

        highlight_color = ("#1f6aa5", "#144870")

        for i, btn in enumerate(self.track_buttons):
            if i == index:
                btn.configure(
                    fg_color=highlight_color,
                    hover_color=highlight_color,
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color=self.default_fg_color,
                    hover_color=self.default_fg_color,
                    text_color="white"
                )
