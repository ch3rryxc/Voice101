import time
import logging
import config

class VoiceEngine:
    def __init__(self, model_name=config.MODEL_NAME, device='cuda'):
        self.model_name = model_name
        self.device = device
        self.tts = None

    def initialize(self):
        logging.info("📦 Importing TTS...")
        start = time.time()
        from TTS.api import TTS 

        logging.info("🔧 Loading XTTS model...")
        self.tts = TTS(self.model_name).to(self.device)

        logging.info(f"✅ XTTS init done in {round(time.time() - start, 2)} sec")

    def speak(self, text: str, sample_path: str, out_path: str = 'outputs/output.wav'):
        if not self.tts:
            raise RuntimeError("❌ TTS not initialized")
        logging.info(f"🎤 Voicing: '{text}'...")
        self.tts.tts_to_file(
            text=text,
            speaker_wav=sample_path,
            language=config.LANG,
            file_path=out_path
        )

        logging.info(f"✅ File saved: {out_path}")