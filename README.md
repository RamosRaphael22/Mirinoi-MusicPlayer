---

# 🎵 Mirinoi Player

Mirinoi is a music player built **100% in Python**, with a graphical interface using **CustomTkinter**, focused on YouTube playlists, automatic playback, shuffle, and visual highlighting of the currently playing track.

---

## 🚀 Features

✔ Modern graphical interface (CustomTkinter)

✔ YouTube Music playlist loading

✔ Automatic playback of the next track (autoplay)

✔ Queue control (next / previous)

✔ Shuffle while preserving the current track

✔ Highlight of the currently playing song

✔ Button-based controls (play, pause, next, prev)

✔ `.csv` file for playlist management

🔜 **In development**

* Real pause (resume from the exact position)
* VLC integration
* Player state machine (IDLE / PLAYING / PAUSED)

---

## 🗂 Project Structure

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
├── models/
│   ├── playlist.py
│   └── track.py
│
├── ui/
│   ├── main_window.py
│   ├── playlist_sidebar.py
│   ├── track_list.py
│   └── player_controls.py
│
├── utils/
│   └── validators.py
│
└── README.md
```

---

## 🧰 Technologies Used

* **Python 3.10+**
* **CustomTkinter**
* **yt-dlp**
* **ffmpeg / ffplay**
* **VLC (planned)**
* **python-vlc (planned)**

---

## 📦 Dependencies

Install the Python dependencies:

```bash
pip install customtkinter yt-dlp
```

⚠️ Make sure the following executables are available in your **PATH**:

* `ffmpeg`
* `ffplay`
* `yt-dlp`

---

## ▶️ How to Run

From the project root:

```bash
python app.py
```

---

## 📄 Playlists (CSV)

The `playlists.csv` file follows this format:

```csv
name,url
My Playlist,https://www.youtube.com/playlist?list=XXXX
```

---

## 🎧 Player Behavior

* Clicking a song starts playback
* The current song is visually highlighted
* When a song ends, the next one plays automatically
* Shuffle preserves the current song when enabled
* Physical controls via buttons

---

## ⚠️ Current Limitations

* Pause is still simulated (stop)
* When paused, the song restarts on play
* This will be solved with **VLC + a state machine**

---

## 🛠 Planned Next Steps

1. Replace `ffplay` with **VLC**
2. Implement real pause (play / pause / resume)
3. Create a player state machine
4. Improve UI ↔ audio synchronization
5. Handle concurrency issues (threads)

---

## 👨‍💻 Author

Project developed by **Raphael Ramos Cavalcante**

Degree: Systems Analysis and Development

Main language: Python 🐍

---

## 🧠 Important Note

This project is **educational** and experimental.

Use public playlists and respect YouTube’s terms of service.

---

