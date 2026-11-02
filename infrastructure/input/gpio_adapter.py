import time
from typing import Optional
from application.ports.input_port import InputTriggerPort
from config.settings import settings


class GpioButtonAdapter(InputTriggerPort):
    """
    Adapter bắt sự kiện nút bấm vật lý qua GPIO Raspberry Pi (Push-to-Talk).
    """

    def __init__(self, button_pin: int = 0):
        self.button_pin = button_pin or settings.GPIO_BUTTON_PIN
        self._gpio_available = False
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.button_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
            self._gpio_available = True
        except (ImportError, RuntimeError):
            self._gpio_available = False

    def wait_for_trigger(self) -> Optional[str]:
        if not self._gpio_available:
            time.sleep(1)
            return None

        # Chờ nút bấm (mức LOW khi nhấn xuống)
        while True:
            if self.GPIO.input(self.button_pin) == self.GPIO.LOW:
                # Bắt đầu thu âm Push-to-Talk ở đây
                return "bật vtv1"
            time.sleep(0.05)

