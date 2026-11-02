import re

# =====================================================================
# BỘ MẪU LỆNH HỆ THỐNG CHUẨN (SINGLE SOURCE OF TRUTH)
# =====================================================================

# 1. TIỀN TỐ Ý ĐỊNH NỘI DUNG (Content Action Guard)
# Khi câu bắt đầu bằng các hành động mở nội dung hoặc có vế muốn xem/nghe,
# tuyệt đối không để rơi vào các lệnh điều khiển thiết bị (như volume, sleep).
CONTENT_INTENT_PREFIX = re.compile(
    r"^\s*(?:mở|bật|tìm|xem|nghe|hát|phát|cho\s+(?:ông|bà|tôi)?\s*(?:nghe|xem))\s+"
    r"(?:nhạc|bài|video|phim|vở|kênh|clip|hài|ca\s+nhạc|kinh|pháp|chương\s+trình)\b",
    re.IGNORECASE
)

CONTENT_INTENT_KEYWORD = re.compile(
    r"\b(?:trên\s+youtube|tìm\s+trên\s+youtube|muốn\s+(?:nghe|xem))\b",
    re.IGNORECASE
)

# 2. CÂU PHỦ ĐỊNH (Negation Guard)
NEGATION_PREFIX = re.compile(
    r"\b(?:đừng|không\s+được|thôi\s+đừng|chớ)\b",
    re.IGNORECASE
)

# 3. MẪU LỆNH TĂNG ÂM LƯỢNG (Word-bounded)
VOLUME_UP_PATTERNS = [
    re.compile(r"\bcho\s+to\s+tiếng(?:\s+(?:lên|hơn|một\s+chút|tí))?\b", re.IGNORECASE),
    re.compile(r"\b(?:tăng|nâng|vặn\s+to|bật\s+to|cho\s+to|mở\s+to)\s+(?:âm\s+lượng|âm|tiếng|volume)\b", re.IGNORECASE),
    re.compile(r"\bto\s+(?:tiếng\s+)?(?:lên|hơn)\b", re.IGNORECASE),
    re.compile(r"\blớn\s+(?:tiếng\s+)?(?:lên|hơn)\b", re.IGNORECASE),
    re.compile(r"\bto\s+tiếng\b", re.IGNORECASE),
    re.compile(r"\bnói\s+to\s+lên\b", re.IGNORECASE),
    re.compile(r"\bbật\s+to\s+lên\b", re.IGNORECASE),
]

# 4. MẪU LỆNH GIẢM ÂM LƯỢNG (Word-bounded)
VOLUME_DOWN_PATTERNS = [
    re.compile(r"\bgiảm\s+(?:âm\s+lượng|âm|tiếng|volume)\b", re.IGNORECASE),
    re.compile(r"\b(?:cho|vặn|bật|nói)\s+(?:nhỏ|bé)\s*(?:lại|đi|xuống|tiếng)?\b", re.IGNORECASE),
    re.compile(r"\b(?:nhỏ|bé)\s+(?:tiếng|lại|đi|xuống|hơn)\b", re.IGNORECASE),
    re.compile(r"\bbật\s+nhỏ\s+lại\b", re.IGNORECASE),
]

# 5. CÁC MẪU LỆNH NỐI TIẾP THEO NGỮ CẢNH (Contextual Follow-ups)
FOLLOWUP_VOLUME_DOWN_PATTERN = re.compile(
    r"^\s*(?:bé|nhỏ|giảm)\s+(?:nữa|thêm|tiếp|nữa\s+đi|thêm\s+chút|tí\s+nữa)\s*$",
    re.IGNORECASE
)
FOLLOWUP_VOLUME_UP_PATTERN = re.compile(
    r"^\s*(?:to|tăng|lớn)\s+(?:nữa|thêm|tiếp|nữa\s+đi|thêm\s+chút|tí\s+nữa)\s*$",
    re.IGNORECASE
)

# 6. MẪU LỆNH TẮT TV / ĐI NGỦ
SLEEP_PATTERNS = [
    re.compile(r"\b(?:tắt\s+(?:tv|tivi|màn\s+hình|máy))\b", re.IGNORECASE),
    re.compile(r"\b(?:đi\s+ngủ|buồn\s+ngủ)(?:\s+đây|\s+rồi)?\b", re.IGNORECASE),
    re.compile(r"\b(?:nghỉ\s+xem(?:\s+(?:tv|tivi))?)\b", re.IGNORECASE),
]

# 7. MẪU LỆNH TẠM DỪNG / TIẾP TỤC
MEDIA_PAUSE_PATTERNS = [
    re.compile(r"\b(?:tạm\s+dừng|dừng\s+lại|dừng\s+video|pause)\b", re.IGNORECASE),
    re.compile(r"\b(?:tiếp\s+tục(?:\s+phát)?|phát\s+tiếp|nghe\s+tiếp|bật\s+lại)\b", re.IGNORECASE),
]

# 8. MẪU LỆNH ĐIỀU HƯỚNG TRANG CHỦ / QUAY LẠI
NAV_HOME_PATTERNS = [
    re.compile(r"\b(?:về\s+(?:trang\s+chủ|màn\s+hình\s+chính)|trang\s+chủ|màn\s+hình\s+chính|thoát\s+ra|home)\b", re.IGNORECASE),
]

NAV_BACK_PATTERNS = [
    re.compile(r"\b(?:quay\s+lại|trở\s+lại|lùi\s+lại|back)\b", re.IGNORECASE),
]

# 9. KÊNH THỜI SỰ VTV TRỰC TIẾP
VTV1_PATTERNS = [
    re.compile(r"^\s*(?:bật|mở|xem|cho\s+(?:ông|bà)\s*xem)?\s*(?:thời\s+sự(?:\s+(?:vtv1|19h|tối))?|vtv1|kênh\s+1)\s*(?:đi(?:\s+cháu)?)?\s*$", re.IGNORECASE),
    re.compile(r"^\s*đến\s+giờ\s+thời\s+sự\s+rồi\s*$", re.IGNORECASE),
]
VTV2_PATTERNS = [
    re.compile(r"\b(?:bật|mở|xem)?\s*vtv2\b", re.IGNORECASE),
]
VTV3_PATTERNS = [
    re.compile(r"\b(?:bật|mở|xem)?\s*vtv3\b", re.IGNORECASE),
]
