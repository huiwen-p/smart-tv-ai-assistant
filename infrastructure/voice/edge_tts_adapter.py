import os
import tempfile
import asyncio
from application.ports.voice_port import VoiceFeedbackPort
from config.settings import settings


class EdgeTtsAdapter(VoiceFeedbackPort):
    """
    Adapter giọng nói tiếng Việt Microsoft Edge-TTS (giọng Hoài My ấm áp, chậm rãi).
    Tự động fallback về Console nếu máy chưa cài thư viện edge-tts.
    """

    def __init__(self, voice: str = "", rate: str = ""):
        self.voice = voice or settings.TTS_VOICE
        self.rate = rate or settings.TTS_RATE
        self._tts_available = False
        try:
            import importlib
            self.edge_tts = importlib.import_module("edge_tts")
            self._tts_available = True
        except ImportError:
            self._tts_available = False

    def speak(self, text: str) -> None:
        print(f"\n[Loa Trợ Lý 🔊]: \"{text}\"")
        if not self._tts_available:
            return

        try:
            asyncio.run(self._play_tts(text))
        except Exception:
            pass

    async def _play_tts(self, text: str):
        communicate = self.edge_tts.Communicate(text, self.voice, rate=self.rate)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        try:
            await communicate.save(temp_path)
            os.system(f'powershell -c "(New-Object Media.SoundPlayer \'{temp_path}\').PlaySync();" >nul 2>&1')
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def play_ding(self):
        print("[Âm báo 🔔 Ting!]")

