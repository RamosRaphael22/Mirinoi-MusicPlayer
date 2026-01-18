import unicodedata
import customtkinter as ctk
from tkinter import messagebox
from ui.playlist_modal import PlaylistModal
from ui.theme import SURFACE, SURFACE_2, SURFACE_HOVER, ACCENT, ACCENT_HOVER, TEXT, STROKE, DANGER_HOVER, TEXT_MUTED, SURFACE_3


# Sidebar UI component for managing playlists
# Displays list of playlists from CSV service
# Allows adding/removing playlists via modal dialog
# Calls callback on playlist selection
# Highlights selected playlist
class PlaylistSidebar(ctk.CTkFrame):
    def __init__(self, parent, csv_service, on_select_callback=None, on_remove_callback=None):
        super().__init__(parent, width=220)

        self.configure(fg_color=SURFACE)

        self.csv_service = csv_service
        self.on_select_callback = on_select_callback
        self.on_remove_callback = on_remove_callback

        self.selected_playlist_id = None
        self.playlist_buttons = {}

        self._all_playlists = []

        self.search_var = ctk.StringVar()

        self._placeholder_text = "Pesquisar playlists..."
        self._placeholder_active = False

        self._build_ui()
        self._load_playlists()

    def _norm(self, s: str) -> str:
        s = s or ""
        s = unicodedata.normalize("NFKD", s)
        s = "".join(ch for ch in s if not unicodedata.combining(ch))
        return s.lower().strip()

    def _build_ui(self):
        self.title = ctk.CTkLabel(
            self,
            text="Playlists",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        self.title.pack(pady=(10, 6))

        self.search_row = ctk.CTkFrame(self, fg_color="transparent")
        self.search_row.pack(fill="x", padx=10, pady=(0, 8))

        self.search_entry = ctk.CTkEntry(
            self.search_row,
            textvariable=self.search_var,
            fg_color=SURFACE_3,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE,
            width=170
        )
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_entry.bind("<FocusIn>", lambda e: self._clear_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self._apply_placeholder())
        self.search_entry.bind("<KeyPress>", lambda e: self._clear_placeholder())
        self._apply_placeholder()

        self.clear_btn = ctk.CTkButton(
            self.search_row,
            text="x",
            width=34,
            height=28,
            fg_color=SURFACE_3,
            hover_color=SURFACE_HOVER,
            text_color=TEXT_MUTED,
            border_width=1,
            border_color=STROKE,
            command=self._clear_search
        )
        self.clear_btn.pack(side="left", padx=(6, 0), pady=(2, 0))

        self.search_var.trace_add("write", lambda *_: (self._apply_playlist_filter(), self._update_clear_button()))
        self._update_clear_button()

        self.scroll = ctk.CTkScrollableFrame(self, height=400, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10)

        self.btn_add = ctk.CTkButton(
            self,
            text="➕ Adicionar",
            command=self._add_playlist_dialog,
            fg_color=SURFACE_2,
            hover_color=SURFACE_HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE
        )
        self.btn_add.pack(fill="x", padx=10, pady=(5, 2))

        self.btn_remove = ctk.CTkButton(
            self,
            text="❌ Remover",
            command=self._remove_selected_playlist,
            fg_color=SURFACE_2,
            hover_color=DANGER_HOVER,
            text_color=TEXT,
            border_width=1,
            border_color=STROKE
        )
        self.btn_remove.pack(fill="x", padx=10, pady=(2, 10))

    def _apply_placeholder(self):
        if self.search_var.get().strip():
            return

        if self.focus_get() == self.search_entry:
            return

        self._placeholder_active = True
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, self._placeholder_text)
        self.search_entry.configure(text_color=TEXT_MUTED)

    def _clear_placeholder(self):
        if not self._placeholder_active:
            return

        self._placeholder_active = False
        self.search_entry.delete(0, "end")
        self.search_entry.configure(text_color=TEXT)

    def _load_playlists(self):
        self._all_playlists = self.csv_service.load_playlists()
        self._apply_playlist_filter()

    def _apply_playlist_filter(self):
        raw = self.search_var.get()
        if self._placeholder_active or raw == self._placeholder_text:
            raw = ""

        query = self._norm(raw)

        if not query:
            filtered = self._all_playlists
        else:
            filtered = [p for p in self._all_playlists if query in self._norm(p.name)]

        self._render_playlists(filtered)

    def _render_playlists(self, playlists):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.playlist_buttons.clear()

        for playlist in playlists:
            btn = ctk.CTkButton(
                self.scroll,
                text=playlist.name,
                anchor="w",
                command=lambda p=playlist: self._select_playlist(p),
                fg_color=SURFACE_2,
                hover_color=SURFACE_HOVER,
                text_color=TEXT,
                border_width=1,
                border_color=STROKE
            )
            btn.pack(fill="x", pady=2, padx=5)
            self.playlist_buttons[playlist.id] = btn

        if self.selected_playlist_id and self.selected_playlist_id in self.playlist_buttons:
            btn = self.playlist_buttons[self.selected_playlist_id]
            btn.configure(
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color="white",
                border_width=0
            )

    def _select_playlist(self, playlist):
        self.selected_playlist_id = playlist.id

        for pid, btn in self.playlist_buttons.items():
            if pid == playlist.id:
                btn.configure(
                    fg_color=ACCENT,
                    hover_color=ACCENT_HOVER,
                    text_color="white",
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

        if self.on_select_callback:
            self.on_select_callback(playlist)

    def _add_playlist_dialog(self):
        modal = PlaylistModal(self)
        result = modal.show()

        if result:
            name, url = result
            self.csv_service.add_playlist(name, url)
            self._load_playlists()

    def _remove_selected_playlist(self):
        if not self.selected_playlist_id:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma playlist para remover."
            )
            return

        confirm = messagebox.askyesno(
            "Remover Playlist",
            "Tem certeza que deseja remover esta playlist?"
        )

        if confirm:
            removed_id = self.selected_playlist_id
            self.csv_service.remove_playlist(removed_id)
            self.selected_playlist_id = None
            self._load_playlists()

            if self.on_remove_callback:
                self.on_remove_callback(removed_id)

    def _clear_search(self):
        self.search_var.set("")
        self._clear_placeholder()
        self._apply_playlist_filter() 
        self._update_clear_button()
        self._apply_placeholder()


    def _update_clear_button(self):    
        raw = self.search_var.get()

        if self._placeholder_active or not raw.strip() or raw == self._placeholder_text:
            self.clear_btn.configure(state="disabled", text_color=TEXT_MUTED)
        else:
            self.clear_btn.configure(state="normal", text_color=TEXT)
