import os
import re
import shutil
import socket
import subprocess
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Optional
from application.ports.device_port import DeviceControllerPort
from config.settings import settings


class ClosedLoopAdbAdapter(DeviceControllerPort):
    """
    Closed-Loop ADB Adapter:
    Quản lý kết nối ADB Wi-Fi tới TV Xiaomi với cơ chế Closed-Loop Control:
    Command ➔ Execute ➔ Observe Result (dumpsys) ➔ Verify Expected State ➔ Success/Retry/Report.
    """

    def __init__(self, target_ip: str = ""):
        self.target_ip = target_ip or settings.TARGET_DEVICE_IP
        self.adb_path = self._locate_adb()
        self.active_device = ""
        if self.target_ip:
            self._connect_wifi()
        self.active_device = self._detect_active_device()

    def _locate_adb(self) -> str:
        which_adb = shutil.which("adb")
        if which_adb:
            return which_adb

        candidates = [
            settings.FALLBACK_ADB_PATH,
            r"D:\android-sdk\platform-tools\adb.exe",
            os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Android\Sdk\platform-tools\adb.exe"),
            "/usr/bin/adb",
            "/usr/local/bin/adb"
        ]
        for candidate in candidates:
            if candidate and os.path.isfile(candidate):
                return candidate

        return "adb"

    @staticmethod
    def _is_port_open(host: str, port: int, timeout: float = 0.3) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                return s.connect_ex((host, port)) == 0
        except Exception:
            return False

    def _get_all_online_devices(self) -> List[str]:
        try:
            res = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace"
            )
            devices = []
            for line in res.stdout.splitlines():
                line = line.strip()
                if not line or line.startswith("List of devices"):
                    continue
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    devices.append(parts[0])
            return devices
        except Exception:
            return []

    def _connect_wifi(self):
        target = self.target_ip.strip()
        if not target:
            return

        ip = target.split(":")[0]
        port = target.split(":")[1] if ":" in target else "5555"

        subprocess.run([self.adb_path, "connect", f"{ip}:{port}"], capture_output=True, timeout=5)

    def _detect_active_device(self) -> str:
        devices = self._get_all_online_devices()
        if not devices:
            return ""

        if self.target_ip:
            ip = self.target_ip.split(":")[0]
            for d in devices:
                if d.startswith(ip):
                    return d

        return devices[0]

    def is_connected(self) -> bool:
        self.active_device = self._detect_active_device()
        return bool(self.active_device)

    def run_shell(self, args: List[str]) -> Tuple[bool, str]:
        if not self.is_connected():
            return False, "Thiết bị chưa kết nối hoặc chưa bật chế độ Gỡ lỗi ADB."

        cmd = [self.adb_path, "-s", self.active_device, "shell"] + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10, encoding="utf-8", errors="replace")
            return res.returncode == 0, res.stdout.strip()
        except Exception as e:
            return False, str(e)

    def send_key(self, key_code: str, repeat: int = 1) -> bool:
        for _ in range(max(1, repeat)):
            ok, _ = self.run_shell(["input", "keyevent", key_code])
            if not ok:
                return False
            time.sleep(0.1)
        return True

    def open_deeplink(self, uri: str) -> Tuple[bool, str]:
        return self.run_shell(["am", "start", "-a", "android.intent.action.VIEW", "-d", uri])

    def launch_app(self, packages: List[str]) -> Tuple[bool, str]:
        for pkg in packages:
            ok, out = self.run_shell(["monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"])
            if ok and "No activities found" not in out:
                return True, f"Đã khởi chạy ứng dụng: {pkg}"
        return False, f"Không thể mở các ứng dụng: {packages}"

    def search_youtube(self, query: str) -> Tuple[bool, str]:
        encoded = urllib.parse.quote(query)
        deep_link = f"vnd.youtube://www.youtube.com/results?search_query={encoded}"
        ok, out = self.open_deeplink(deep_link)
        if ok and "Activity not started" not in out:
            return True, f"Đã mở YouTube tìm: '{query}'"
        return self.open_deeplink(f"https://www.youtube.com/results?search_query={encoded}")

    def open_vtv_channel(self, channel_code: str = "vtv1") -> Tuple[bool, str]:
        ch_num = "1"
        if "3" in channel_code:
            ch_num = "3"
        elif "2" in channel_code:
            ch_num = "2"

        app_link = f"https://vtvgo.vn/xem-truc-tuyen-kenh-vtv{ch_num}-{ch_num}.html"
        ok, out = self.open_deeplink(app_link)
        if ok and "Activity not started" not in out and "unable to resolve Intent" not in out:
            return True, f"Đã mở luồng VTV{ch_num} qua VTVgo App Link."

        vtv_packages = [
            "vn.vtv.vtvgo.smarttv",
            "vn.vtv.vtvgo",
            "com.vtv.vtvgo"
        ]
        ok, out = self.launch_app(vtv_packages)
        if ok:
            return True, "Đã mở ứng dụng VTVgo trên thiết bị."

        return self.search_youtube(f"VTV{ch_num} trực tiếp thời sự")

    def get_current_focus(self) -> Optional[str]:
        """Closed-Loop Observation: Kiểm tra ứng dụng / Activity đang hiển thị."""
        ok, out = self.run_shell(["dumpsys", "window"])
        if not ok or not out:
            return None
        for line in out.splitlines():
            if "mCurrentFocus" in line or "mFocusedApp" in line:
                return line.strip()
        return None

