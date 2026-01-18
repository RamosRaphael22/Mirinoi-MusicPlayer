# 🎵 Mirinoi Player

**Mirinoi** is a desktop music player built **100% in Python**, featuring a modern graphical interface using **CustomTkinter** and focused on **YouTube Music playlist streaming**, queue management, and accurate real-time playback control using **VLC**.

The project emphasizes **clean architecture**, separation of concerns, and a responsive UI with real playback state.

---

## 🚀 Features

* ✅ Modern graphical interface (**CustomTkinter**)
* ✅ Centralized UI theming system (`ui/theme.py`)
* ✅ YouTube Music playlist loading
* ✅ Background playlist loading (**non-blocking UI**)
* ✅ Queue navigation (**next / previous**)
* ✅ **Shuffle** with order restoration
* ✅ **Playlist loop mode** (optional)
* ✅ Visual highlight of the currently playing track
* ✅ Unified **Play / Pause** button (synced with player state)
* ✅ **Real pause & resume** (continues from the exact position)
* ✅ **Interactive playback progress bar** (**seek support**)
* ✅ **Current playback time / total duration** display
* ✅ **Volume control slider** (real-time)
* ✅ VLC-based audio streaming
* ✅ `.csv` file for playlist persistence

---

## 🎨 UI Theme System

Mirinoi uses a centralized theme system located at:

* `ui/theme.py`

This file stores UI colors as hex variables, enabling:

* consistent visual identity
* easy theme adjustments
* cleaner UI components
* styling separated from layout logic

UI components import colors directly from `theme.py` to avoid hardcoded values.

---

## 🗂 Project Structure

```text
Mirinoi/
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
│   ├── player_controls.py
│   └── theme.py
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
4. **yt-dlp (Python library)** extracts playlist entries/metadata
5. Tracks are rendered in the UI
6. The user selects a track
7. **yt-dlp (Python library)** extracts a direct audio stream URL
8. **VLC** streams the audio
9. `QueueManager` controls navigation, shuffle, and loop behavior
10. `AudioPlayer` manages playback lifecycle, state, volume, seek, and progress tracking

---

## 🧠 Architecture & Design Decisions

### 🎨 CustomTkinter

Chosen for its modern look, theming support, and improved UX compared to standard Tkinter.

### 🎧 VLC + python-vlc

Used to support:

* real pause / resume
* seek to any playback position
* playback state inspection
* volume control
* accurate playback timing

The playback state machine (`STOPPED / PLAYING / PAUSED`) lives **exclusively** inside `AudioPlayer`.

### 🎥 yt-dlp (Python library)

Used **as a Python library** to retrieve playlist metadata and generate direct audio stream URLs, without relying on external executables.

This approach avoids subprocess calls, prevents console windows from appearing, and simplifies application packaging.

### 🧵 Threading

All blocking operations (yt-dlp extraction and VLC startup) run in background threads to keep the UI responsive.

### 🗂 CSV Storage

A simple and portable solution for playlist persistence, easily replaceable by a database in the future.

### 🧱 Layered Architecture

* UI layer never interacts directly with VLC or subprocesses
* Core layer encapsulates playback logic, queue management, and external tools
* Clear separation of responsibilities between modules

---

## 🧰 Technologies Used

* **Python 3.10+**
* **CustomTkinter**
* **yt-dlp (Python library)**
* **VLC**
* **python-vlc**
* **FFmpeg** (optional, recommended)

---

## 📦 Installation

### Python Dependencies

```bash
pip install customtkinter yt-dlp python-vlc
```

---

## 🖥 System Requirements

### 🔹 VLC Media Player (required)

VLC is used as the **audio playback engine**, providing:

* native streaming support
* real pause / resume
* seek and volume control
* reliable playback state detection

Download:
[https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)

---

### 🔹 yt-dlp (Python library)

Used to:

* fetch playlist metadata
* generate direct audio streaming URLs

yt-dlp is used **as a Python library**, not as an external executable.
No system-wide installation or PATH configuration is required.

---

### 🔹 FFmpeg (optional but recommended)

Recommended for:

* yt-dlp fallback scenarios
* improved compatibility with edge-case formats

Download:
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Verify installation:

```bash
ffmpeg -version
```

---

## ▶️ How to Run

From the project root:

```bash
python app.py
```

---

## 📄 Playlists (CSV)

Example:

```csv
name,url
My Playlist,https://www.youtube.com/playlist?list=XXXX
```

If `playlists.csv` does not exist, the application will create it automatically.

---

## 🎧 Player Behavior

* Clicking a song starts playback
* The current track is visually highlighted
* Play/Pause is a single toggle button
* Playback resumes from the exact paused position
* The progress bar updates in real time
* Users can **seek freely** by dragging the progress bar
* Playback time and total duration are displayed
* Volume can be adjusted during playback
* When a track ends, the next one plays automatically
* Shuffle preserves the current track
* Loop restarts the playlist when enabled

---

## ⚠️ Current Limitations

* Playback depends on network availability and YouTube stream stability
* Initial stream loading time may vary depending on connection quality
* VLC streaming behavior depends on YouTube servers

---

## 🛠 Planned Improvements

1. Improved error feedback in the UI
2. Keyboard shortcuts
3. Persist user settings (volume, last playlist)
4. Packaging as a standalone executable

---

## 👨‍💻 Author

Project developed by **Raphael Ramos Cavalcante**
Degree: Systems Analysis and Development
Main language: Python 🐍

---

## 🧠 Important Note

This project is **educational and experimental**.

Use public playlists and respect YouTube’s terms of service.
