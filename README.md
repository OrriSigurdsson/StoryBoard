# 📌 Story Whiteboard

A minimal, canvas-based whiteboard app for planning stories using draggable notes.

Built with **Python + Tkinter**.

---

## ✨ Features

* 🗒 Create notes with a double-click
* ✏ Edit notes with right-click
* 🏷 Tag system (Scene, Character, Twist, World)
* 🎨 Custom color picker per note
* 🔢 Automatic word count per note
* 🖱 Drag & snap-to-grid movement
* 🔍 Zoom with:

  * Ctrl + Mouse Wheel
  * Zoom slider
* 📜 Scrollable large canvas
* 💾 Save / Load board as JSON

---

## 🖼 How It Works

Each note contains:

* **Title**
* Up to **10 bullet points**
* **Tag**
* **Custom color**
* **Automatic word count**

Notes are displayed on a scalable canvas and can be freely arranged to visually plan your story structure.

---

## 🛠 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/story-whiteboard.git
cd story-whiteboard
```

### 2️⃣ Run the app

Make sure you have Python 3 installed.

```bash
python main.py
```

No external libraries required — Tkinter comes with Python.

---

## 🧠 Controls

| Action       | Control              |
| ------------ | -------------------- |
| Create Note  | Double Left Click    |
| Edit Note    | Right Click          |
| Drag Note    | Left Click + Drag    |
| Snap to Grid | Automatic on release |
| Zoom         | Ctrl + Mouse Wheel   |
| Zoom Slider  | Toolbar              |
| Save Board   | Save Button          |
| Load Board   | Load Button          |

---

## 💾 File Format

Boards are saved as:

```json
[
  {
    "x": 200,
    "y": 300,
    "title": "Opening Scene",
    "bullets": ["Hero wakes up", "Strange noise outside"],
    "tag": "Scene",
    "color": "#fff59d"
  }
]
```

---

## 🚀 Future Improvements (Planned)

* Resize notes with drag handles
* Connect notes with lines
* Infinite canvas expansion
* Export to PDF
* Dark mode
* Multi-board project support
* Keyboard shortcuts
* Scene statistics panel

---

## 🎯 Purpose

This project was built to:

* Help writers visually organize ideas
* Replace physical sticky notes
* Create a flexible, interactive planning board

---

## 📄 License

MIT License — free to use and modify.

---

If you’d like, I can also:

* Make it look more impressive / professional
* Add screenshots section template
* Add badges (Python version, license, etc.)
* Write a “Developer Notes” section
* Help you choose a good repo name

What vibe do you want for your GitHub — clean student project or polished indie tool? 😈
