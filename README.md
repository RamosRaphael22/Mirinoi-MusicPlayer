---

# 🎵 Mirinoi Player

Mirinoi é um player de músicas feito **100% em Python**, com interface gráfica em **CustomTkinter**, focado em playlists do YouTube, reprodução automática, shuffle e destaque visual da música atual.

---

## 🚀 Funcionalidades

✔ Interface gráfica moderna (CustomTkinter)

✔ Carregamento de playlists do YouTube Music

✔ Reprodução automática da próxima faixa (autoplay)

✔ Controle de fila (next / previous)

✔ Shuffle com preservação da música atual

✔ Highlight da música em reprodução

✔ Controle por botões (play, pause, next, prev)

✔ Arquivo `.csv` para gerenciar playlists

🔜 **Em desenvolvimento**

* Pause real (retomar do ponto exato)
* Integração com VLC
* Máquina de estados do player (IDLE / PLAYING / PAUSED)

---

## 🗂 Estrutura do Projeto

```
Mirinoi/
│
├── app.py
├── playlists.csv
│
├── core/
│   ├── audio_player.py
│   ├── queue_manager.py
│   ├── csv_service.py
│   └── yt_service.py
│
├── ui/
│   ├── main_window.py
│   ├── playlist_sidebar.py
│   ├── track_list.py
│   └── player_controls.py
│
└── README.md
```

---

## 🧰 Tecnologias Utilizadas

* **Python 3.10+**
* **CustomTkinter**
* **yt-dlp**
* **ffmpeg / ffplay**
* **VLC (planejado)**
* **python-vlc (planejado)**

---

## 📦 Dependências

Instale as dependências Python:

```bash
pip install customtkinter yt-dlp
```

⚠️ Certifique-se de que os executáveis abaixo estejam no **PATH**:

* `ffmpeg`
* `ffplay`
* `yt-dlp`

---

## ▶️ Como Executar

Na raiz do projeto:

```bash
python app.py
```

---

## 📄 Playlists (CSV)

O arquivo `playlists.csv` segue o formato:

```csv
nome,url
Minha Playlist,https://www.youtube.com/playlist?list=XXXX
```

---

## 🎧 Funcionamento do Player

* Clicar em uma música inicia a reprodução
* A música atual é destacada visualmente
* Ao terminar, a próxima toca automaticamente
* Shuffle mantém a música atual ao ativar
* Controles físicos via botões

---

## ⚠️ Limitações Atuais

* Pause ainda é simulado (stop)
* Ao pausar, a música reinicia ao dar play
* Isso será resolvido com **VLC + máquina de estados**

---

## 🛠 Próximos Passos Planejados

1. Substituir `ffplay` por **VLC**
2. Implementar pause real (play / pause / resume)
3. Criar máquina de estados do player
4. Melhorar sincronização UI ↔ áudio
5. Tratar erros de concorrência (threads)

---

## 👨‍💻 Autor

Projeto desenvolvido por **Raphael Ramos Cavalcante**

Curso: Análise e Desenvolvimento de Sistemas

Linguagem principal: Python 🐍

---

## 🧠 Observação Importante

Este projeto é **educacional** e experimental.

Use playlists públicas e respeite os termos do YouTube.

---
