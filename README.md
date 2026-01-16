---

# 🎵 Mirinoi Player

**Mirinoi** is a desktop music player built **100% in Python**, featuring a modern graphical interface using **CustomTkinter** and focused on **YouTube playlist streaming**, queue management, shuffle, loop, and accurate playback control using **VLC**.

The project emphasizes clean architecture, separation of concerns, and real-time audio control without blocking the UI.

---

## 🚀 Features

✔ Modern graphical interface (CustomTkinter)

✔ YouTube Music playlist loading

✔ Background playlist loading (non-blocking UI)

✔ Queue control (next / previous)

✔ Shuffle while preserving the current track

✔ Loop playlist when finished (optional)

✔ Visual highlight of the currently playing track

✔ Unified **Play / Pause** button

✔ **Real pause & resume** (continues from the exact position)

✔ VLC-based audio playback

✔ `.csv` file for playlist persistence

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

## 🔁 Application Flow

1. The application starts and loads playlists from `playlists.csv`
2. Playlists are rendered in the sidebar
3. The user selects a playlist
4. **yt-dlp** fetches track metadata using flat playlist extraction
5. The track list is rendered in the UI
6. The user selects a track
7. **yt-dlp** generates a direct audio stream URL
8. **VLC** streams the audio
9. `QueueManager` controls navigation, shuffle, and loop
10. `AudioPlayer` manages playback state and lifecycle

---

## 🧠 Architecture & Design Decisions

### 🎨 CustomTkinter

Chosen for its modern look, theming support, and better UX compared to standard Tkinter.

### 🎧 VLC + python-vlc

Used instead of `ffplay` to support:

* real pause / resume
* playback state inspection
* better control over streaming behavior

The playback state machine (`STOPPED / PLAYING / PAUSED`) lives **exclusively** inside `AudioPlayer`.

### 🎥 yt-dlp

Used to retrieve playlist metadata and generate direct audio stream URLs without relying on the official YouTube API.

### 🧵 Threading

All blocking operations (yt-dlp execution and VLC startup) run in background threads to keep the UI responsive.

### 🗂 CSV Storage

A simple, portable solution for playlist persistence, easily replaceable by a database in the future.

### 🧱 Layered Architecture

* UI layer never spawns subprocesses
* Core layer encapsulates playback, queues, and external tools
* Clear responsibility boundaries between modules

---

## 🧰 Technologies Used

* **Python 3.10+**
* **CustomTkinter**
* **yt-dlp**
* **VLC**
* **python-vlc**
* **ffmpeg** (dependency of VLC)

---

## 📦 Dependencies

### Python Dependencies

Install the required Python packages:

```bash
pip install customtkinter yt-dlp python-vlc
```

---

### System Requirements

The application relies on the following external tools:

#### 🔹 VLC Media Player (required)

VLC is used as the **audio playback engine**, providing:

* Native streaming support
* Real pause / resume functionality
* Reliable playback state detection

> ⚠️ VLC must be installed on the system.
> The VLC executable **does not need** to be available in `PATH`, but it is recommended.

Download: [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)

---

#### 🔹 yt-dlp (required, must be in PATH)

`yt-dlp` is used to:

* Fetch playlist metadata
* Generate direct audio streaming URLs from YouTube

Make sure `yt-dlp` is accessible from the command line:

```bash
yt-dlp --version
```

---

#### 🔹 FFmpeg (optional but recommended)

FFmpeg is **not required by VLC**, as VLC ships with its own internal decoding libraries.

However, FFmpeg is **recommended** because:

* `yt-dlp` may rely on FFmpeg in fallback scenarios
* Some formats and edge cases require FFmpeg for best compatibility

If installed, ensure it is available in `PATH`:

```bash
ffmpeg -version
```

---

### Dependency Summary

| Dependency       | Required    | Notes                                |
| ---------------- | ----------- | ------------------------------------ |
| Python 3.10+     | ✅           | Core runtime                         |
| CustomTkinter    | ✅           | UI framework                         |
| yt-dlp           | ✅           | YouTube metadata & streaming URLs    |
| python-vlc       | ✅           | Python bindings for VLC              |
| VLC Media Player | ✅           | Audio playback engine                |
| FFmpeg           | ⚠️ Optional | Recommended for yt-dlp compatibility |

---

### ⚠️ Important Notes

* VLC **does not depend on FFmpeg being installed system-wide**
* FFmpeg is only required for `yt-dlp` in specific scenarios
* All blocking operations run in background threads to keep the UI responsive

---

## ▶️ How to Run

From the project root:

```bash
python app.py
```

---

## 📄 Playlists (CSV)

The `playlists.csv` file format:

```csv
name,url
My Playlist,https://www.youtube.com/playlist?list=XXXX
```

---

## 🎧 Player Behavior

* Clicking a song starts playback
* The current track is visually highlighted
* **Play/Pause is a single toggle button**
* Pause resumes from the exact position
* When a track ends, the next one plays automatically
* Shuffle preserves the current track
* Loop restarts the playlist when enabled

---

## ⚠️ Current Limitations

* Playback depends on external tools being available in PATH
* Network instability may affect stream startup time
* VLC streaming behavior depends on YouTube servers

---

## 🛠 Planned Improvements

1. Dependency installation script (Windows / Linux)
2. Better error feedback in the UI
3. Playback progress bar
4. Volume control
5. Keyboard shortcuts
6. Packaging as a standalone executable

---

## 👨‍💻 Author

Project developed by **Raphael Ramos Cavalcante**

Degree: Systems Analysis and Development
Main language: Python 🐍

---

## 🧠 Important Note

This project is **educational and experimental**.

Use public playlists and respect YouTube’s terms of service.

---
