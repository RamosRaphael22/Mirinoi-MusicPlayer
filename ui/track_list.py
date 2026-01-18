import unicodedata
import customtkinter as ctk
from ui.theme import SURFACE, SURFACE_2, SURFACE_HOVER, ACCENT, ACCENT_HOVER, TEXT, STROKE, TEXT_MUTED


# UI component to display and manage the list of tracks
# Allows track selection and highlights the selected track
# Calls a callback when a track is selected
# Provides method to load tracks into the list
# Allows setting highlight on a specific track
class TrackList(ctk.CTkFrame):
    def __init__(self, parent, on_track_selected=None):
        super().__init__(parent)

        self.configure(fg_color=SURFACE)

        self.on_track_selected = on_track_selected

        self.tracks = []
        self._all_tracks = []

        self.selected_index = None
        self.track_buttons = []

        self.default_fg_color = None
        self.highlighted_index = None

        self.search_var = ctk.StringVar()

        self._build_ui()

    def _norm(self, s: str) -> str:
        s = s or ""
        s = unicodedata.normalize("NFKD", s)
        s = "".join(ch for ch in s if not unicodedata.combining(ch))
        return s.lower().strip()

    def _build_ui(self):
        self.title = ctk.CTkLabel(
            self,
            text="Músicas",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        self.title.pack(pady=(10, 6))

        # Search bar
        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Pesquisar músicas...",
            fg_color=SURFACE_2,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE
        )
        self.search_entry.pack(fill="x", padx=10, pady=(0, 8))
        self.search_var.trace_add("write", lambda *_: self._apply_track_filter())

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)

    def show_loading(self):
        self._all_tracks = []
        self.tracks = []
        self.selected_index = None
        self.highlighted_index = None

        self.search_var.set("")  # limpa busca ao carregar

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.track_buttons.clear()
        self.default_fg_color = None

        label = ctk.CTkLabel(
            self.scroll,
            text="Carregando músicas...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_MUTED
        )
        label.pack(pady=20)

    def load_tracks(self, tracks):
        self._all_tracks = tracks or []
        self.search_var.set("")  # opcional: reset ao trocar playlist
        self._apply_track_filter()

    def _apply_track_filter(self):
        query = self._norm(self.search_var.get())

        if not query:
            filtered = self._all_tracks
        else:
            filtered = []
            for t in self._all_tracks:
                hay = f"{t.title} {t.artist or ''}"
                if query in self._norm(hay):
                    filtered.append(t)

        self._render_tracks(filtered)

    def _render_tracks(self, tracks):
        self.tracks = tracks
        self.selected_index = None
        self.highlighted_index = None

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.track_buttons.clear()
        self.default_fg_color = None

        if not tracks:
            label = ctk.CTkLabel(
                self.scroll,
                text="Nenhuma música encontrada.",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_MUTED
            )
            label.pack(pady=20)
            return

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
                command=lambda i=index: self._select_track(i),
                fg_color=SURFACE_2,
                hover_color=SURFACE_HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE
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

        for i, btn in enumerate(self.track_buttons):
            if i == index:
                btn.configure(
                    fg_color=ACCENT,
                    hover_color=ACCENT_HOVER,
                    text_color=TEXT,
                    border_width=0
                )
            else:
                btn.configure(
                    fg_color=SURFACE_2,
                    hover_color=SURFACE_HOVER,
                    text_color=TEXT,
                    border_width=1,
                    border_color=STROKE
                )
