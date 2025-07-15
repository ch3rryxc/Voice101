# 🎙️ Voice101

**Voice101** is a desktop application with a GUI built using Python that synthesizes speech using XTTS v2 and a provided voice preset (`.wav`).

---

## 🚀 Features

- Text-to-speech generation using voice samples.
- Multi-threaded for smooth performance.
- GUI with a dark theme and responsive elements.
- Easy playback of generated audio.
- Configuration for language, preset, and output directories.

---

## 📦 Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure you have **CUDA** installed and a compatible GPU with **at least 4 GB VRAM**.

3. Place your `.wav` voice presets in the `presets/` folder.

---

## ⚙️ Configuration

Edit `config.py`:

```python
LANGUAGE = 'en'          # TTS language ('en', 'ru', etc.)
MODEL_NAME = ''          # You can leave it as in the config
DEVICE = 'cuda'          # What will app run on: GPU (cuda) or CPU
```

---

## 🎧 What is a voice preset?

A preset is a short clean `.wav` file (usually 5–10 seconds) of a speaker's voice. XTTS uses this to mimic the voice.

**Recommendations:**

- One `.wav` per speaker
- Clean, clear, no background noise or effects
- Language in recording should match synthesis language

---

## 💻 System Requirements

| Component         | Minimum Requirement           |
|------------------|-------------------------------|
| GPU              | NVIDIA with 4+ GB VRAM       |
| CUDA             | Version ≥ 11.6                |
| RAM              | 8 GB (16+ GB recommended)     |
| OS               | Windows / Linux               |
| Python           | 3.8–3.11                      |

---

## 🏁 Running

```bash
python gui.py
```

---

## 📝 License

MIT — free to use, modify, and distribute.
