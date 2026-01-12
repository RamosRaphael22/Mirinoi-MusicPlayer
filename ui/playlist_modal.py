import customtkinter as ctk
from tkinter import Toplevel, StringVar
from tkinter import messagebox

from utils.validators import is_valid_url


class PlaylistModal(Toplevel):
    def __init__(self, parent, title="Nova Playlist"):
        super().__init__(parent)

        # 🔹 Tema dark garantido
        ctk.set_appearance_mode("dark")

        self.title(title)
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()  # modal

        self.result = None

        self.name_var = StringVar()
        self.url_var = StringVar()

        self._build_ui()

        # 🔹 UX
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())

    # 🔹 Construção da UI
    def _build_ui(self):
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Nome
        name_label = ctk.CTkLabel(container, text="Nome da playlist:")
        name_label.pack(anchor="w", pady=(0, 2))

        name_entry = ctk.CTkEntry(container, textvariable=self.name_var)
        name_entry.pack(fill="x")
        name_entry.focus()

        # URL
        url_label = ctk.CTkLabel(container, text="URL da playlist:")
        url_label.pack(anchor="w", pady=(10, 2))

        url_entry = ctk.CTkEntry(container, textvariable=self.url_var)
        url_entry.pack(fill="x")

        # Botões
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=15)

        add_btn = ctk.CTkButton(
            btn_frame,
            text="Adicionar",
            command=self._on_ok
        )
        add_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#444",
            hover_color="#555",
            command=self._on_cancel
        )
        cancel_btn.pack(side="left", padx=5)

    # 🔹 Ação OK
    def _on_ok(self):
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()

        if not name or not url:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        if not is_valid_url(url):
            messagebox.showwarning("Erro", "URL inválida do YouTube.")
            return

        self.result = (name, url)
        self.destroy()

    # 🔹 Ação Cancelar
    def _on_cancel(self):
        self.result = None
        self.destroy()

    # 🔹 Método para exibir modal
    def show(self):
        self.wait_window()
        return self.result