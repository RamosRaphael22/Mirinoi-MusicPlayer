import customtkinter as ctk
from tkinter import messagebox


class PlaylistSidebar(ctk.CTkFrame):
    def __init__(self, parent, csv_service, on_select_callback=None):
        super().__init__(parent, width=220)
        self.csv_service = csv_service
        self.on_select_callback = on_select_callback

        self.selected_playlist_id = None
        self.playlist_buttons = {}

        self._build_ui()
        self._load_playlists()

    # 🔹 Construção da UI
    def _build_ui(self):
        self.title = ctk.CTkLabel(
            self,
            text="Playlists",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title.pack(pady=10)

        self.scroll = ctk.CTkScrollableFrame(self, height=400)
        self.scroll.pack(fill="both", expand=True, padx=5)

        self.btn_add = ctk.CTkButton(
            self,
            text="➕ Adicionar",
            command=self._add_playlist_dialog
        )
        self.btn_add.pack(fill="x", padx=10, pady=(5, 2))

        self.btn_remove = ctk.CTkButton(
            self,
            text="❌ Remover",
            fg_color="#8b0000",
            hover_color="#a00000",
            command=self._remove_selected_playlist
        )
        self.btn_remove.pack(fill="x", padx=10, pady=(2, 10))

    # 🔹 Carrega playlists do CSV
    def _load_playlists(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.playlist_buttons.clear()

        playlists = self.csv_service.load_playlists()

        for playlist in playlists:
            btn = ctk.CTkButton(
                self.scroll,
                text=playlist["name"],
                anchor="w",
                command=lambda p=playlist: self._select_playlist(p)
            )
            btn.pack(fill="x", pady=2, padx=5)

            self.playlist_buttons[playlist["id"]] = btn

    # 🔹 Seleção de playlist
    def _select_playlist(self, playlist):
        self.selected_playlist_id = playlist["id"]

        for pid, btn in self.playlist_buttons.items():
            btn.configure(fg_color="#1f6aa5" if pid == playlist["id"] else None)

        if self.on_select_callback:
            self.on_select_callback(playlist)

    # 🔹 Dialog para adicionar playlist
    def _add_playlist_dialog(self):
        dialog = ctk.CTkInputDialog(
            title="Nova Playlist",
            text="Nome da playlist:"
        )
        name = dialog.get_input()

        if not name:
            return

        dialog = ctk.CTkInputDialog(
            title="Nova Playlist",
            text="URL da playlist:"
        )
        url = dialog.get_input()

        if not url:
            return

        self.csv_service.add_playlist(name, url)
        self._load_playlists()

    # 🔹 Remove playlist selecionada
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
            self.csv_service.remove_playlist(self.selected_playlist_id)
            self.selected_playlist_id = None
            self._load_playlists()
