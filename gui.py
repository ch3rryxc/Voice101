import customtkinter as ctk
import os
import threading
import logging
import sys
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage

from voice import VoiceEngine

# Constants
PRESET_DIR = "presets"
OUTPUT_DIR = "outputs"
os.makedirs(PRESET_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string)
        self.widget.see("end")
        self.widget.configure(state="disabled")
    def flush(self):
        pass

class Voice101App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Voice101")
        self.geometry("900x600")
        self.resizable(False, False)
        self.wm_attributes("-alpha", 0.95)

        self.engine = VoiceEngine()
        self.last_presets = []

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)
        self.tts_tab = self.tabview.add("TTS")

        self.build_tts_tab()
        self.init_engine()
        self.watch_presets()

    def build_tts_tab(self):
        self.status_label = ctk.CTkLabel(self.tts_tab, text="Voice101 — Text-to-Speech Interface", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.text_entry = ctk.CTkEntry(self.tts_tab, width=600, placeholder_text="Enter text...")
        self.text_entry.pack(pady=10)

        self.preset_combo = ctk.CTkComboBox(self.tts_tab, values=[], width=300)
        self.preset_combo.pack(pady=5)

        self.buttons_frame = ctk.CTkFrame(self.tts_tab, fg_color="transparent")
        self.buttons_frame.pack(pady=10)

        icon_speak = CTkImage(Image.open("icons/speak.png"), size=(20, 20))
        icon_play = CTkImage(Image.open("icons/play.png"), size=(20, 20))
        icon_clear = CTkImage(Image.open("icons/clear.png"), size=(20, 20))

        self.speak_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Speak",
            image=icon_speak,
            compound="left",
            command=self.start_speaking,
            corner_radius=10,
            fg_color="#2a2a2a",
            hover_color="#3a3a3a"
        )
        self.speak_btn.pack(side="left", padx=10)

        self.play_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Play",
            image=icon_play,
            compound="left",
            command=self.play_audio,
            corner_radius=10,
            fg_color="#2a2a2a",
            hover_color="#3a3a3a"
        )
        self.play_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Clear",
            image=icon_clear,
            compound="left",
            command=self.clear_console,
            corner_radius=10,
            fg_color="#2a2a2a",
            hover_color="#3a3a3a"
        )
        self.clear_btn.pack(side="left", padx=10)

        self.console = ctk.CTkTextbox(self.tts_tab, width=800, height=250, corner_radius=10)
        self.console.pack(padx=10, pady=10)
        self.console.configure(state="disabled")

        sys.stdout = TextRedirector(self.console)
        sys.stderr = TextRedirector(self.console)
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', stream=sys.stdout)

    def clear_console(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

    def refresh_presets(self):
        files = [f for f in os.listdir(PRESET_DIR) if f.lower().endswith('.wav')]
        if files != self.last_presets:
            self.last_presets = files
            self.preset_combo.configure(values=files)
            if files:
                self.preset_combo.set(files[0])
            logging.info("🔄 Preset list updated.")

    def watch_presets(self):
        self.refresh_presets()
        self.after(1000, self.watch_presets)

    def init_engine(self):
        def init():
            try:
                self.status_label.configure(text="🔄 Loading XTTS...")
                self.engine.initialize()
                self.status_label.configure(text="✅ XTTS ready")
            except Exception as e:
                logging.error(f"❌ Error: {e}")
                self.status_label.configure(text="Error")
        threading.Thread(target=init, daemon=True).start()

    def start_speaking(self):
        text = self.text_entry.get().strip()
        preset = self.preset_combo.get()

        if not text:
            messagebox.showwarning("Input required", "Please enter text to synthesize.")
            return
        if not preset:
            messagebox.showwarning("No preset selected", "Please choose a voice preset.")
            return

        preset_path = os.path.join(PRESET_DIR, preset)
        if not os.path.isfile(preset_path):
            messagebox.showwarning("File not found", "Selected preset not found.")
            return

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        preset_name = os.path.splitext(preset)[0]
        out_path = os.path.join(OUTPUT_DIR, f"output_{timestamp}_{preset_name}.wav")
        self.current_output_path = out_path

        self.status_label.configure(text="🗣 Generating speech...")
        self.speak_btn.configure(state="disabled")

        threading.Thread(target=self.speak, args=(text, preset_path, out_path), daemon=True).start()

    def speak(self, text, preset_path, out_path):
        try:
            self.engine.speak(text, preset_path, out_path)
            self.status_label.configure(text=f"✅ Saved: {os.path.basename(out_path)}")
        except Exception as e:
            logging.error(f"Error during synthesis: {e}")
            self.status_label.configure(text="Error")
        finally:
            self.speak_btn.configure(state="normal")

    def play_audio(self):
        if not hasattr(self, "current_output_path") or not os.path.exists(self.current_output_path):
            messagebox.showwarning("No file", "Generate audio before playing.")
            return
        try:
            data, samplerate = sf.read(self.current_output_path)
            sd.play(data, samplerate)
            sd.wait()
        except Exception as e:
            logging.error(f"Playback error: {e}")

if __name__ == '__main__':
    app = Voice101App()
    app.mainloop()
