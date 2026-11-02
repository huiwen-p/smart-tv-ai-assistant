from application.ports.voice_port import VoiceFeedbackPort


class ConsoleVoiceAdapter(VoiceFeedbackPort):
    def speak(self, text: str) -> None:
        print(f"\n[Loa Trợ Lý 🔊]: \"{text}\"")

    def play_ding(self) -> None:
        print("[Âm báo 🔔 Ting!]")

