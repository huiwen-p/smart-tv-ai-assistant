import json
import urllib.request
import urllib.error
import re
from typing import Optional, List, Dict, Any
from config.settings import settings
from domain.entities.intent import TVActionType, ResolvedCommand
from domain.entities.content_item import ContentItem
from application.ports.ai_resolver_port import BaseAIResolverPort
from application.intent.intent_classifier import SystemIntentClassifier


SYSTEM_PROMPT = """Bạn là trợ lý AI chuyên điều khiển TV thông minh cho người cao tuổi (ông bà) tại Việt Nam.
Nhiệm vụ: Phân tích khẩu ngữ tự nhiên, đời thường của ông bà và chuyển đổi thành cấu trúc điều khiển an toàn cho TV.

QUY TẮC CỐT TỬ:
1. KHÔNG tự ý bịa ra ID nội dung hoặc câu lệnh kỹ thuật.
2. Nếu câu nói yêu cầu điều khiển hệ thống (âm lượng, tắt TV, tạm dừng, trang chủ):
   - To tiếng, nói to, cho to lên, tăng âm, volume to... -> action_type: "SYSTEM_CONTROL", target: "volume_up"
   - Nhỏ tiếng, cho bé lại, giảm âm, nói nhỏ... -> action_type: "SYSTEM_CONTROL", target: "volume_down"
   - Tắt TV, đi ngủ, nghỉ xem, buồn ngủ... -> action_type: "SYSTEM_CONTROL", target: "sleep"
   - Tạm dừng, dừng lại, phát tiếp... -> action_type: "SYSTEM_CONTROL", target: "pause"
   - Về màn hình chính, trang chủ, thoát ra... -> action_type: "SYSTEM_CONTROL", target: "home"
   - Quay lại, trở lại... -> action_type: "SYSTEM_CONTROL", target: "back"
3. Kênh thời sự trực tiếp:
   - Thời sự, VTV1, tin tức tối -> action_type: "PLAY_LIVE_TV", target: "vtv1"
   - VTV2 -> action_type: "PLAY_LIVE_TV", target: "vtv2"
   - VTV3 -> action_type: "PLAY_LIVE_TV", target: "vtv3"
4. Xem video / nội dung:
   - Nếu danh sách ứng viên (Candidates) được cung cấp, hãy chọn `content_id` phù hợp nhất từ danh sách đó nếu câu nói của ông bà khớp với ứng viên.
   - Nếu câu nói quá mơ hồ hoặc có 2 bài tương đương mà bà không nói rõ, đặt action_type: "CLARIFY" và đưa ra câu hỏi lễ phép để làm rõ.
   - Nếu không khớp ứng viên nào nhưng bà muốn tìm nội dung mới: action_type: "SEARCH_YOUTUBE", query: "từ khóa".

Quy tắc câu trả lời (feedback):
- Luôn là một câu nói xưng hô "Dạ, cháu..." ấm áp, kính cẩn, lễ phép, nói ngắn gọn, rõ ràng.
Ví dụ: "Dạ, cháu đang bật thời sự VTV1 cho ông bà ạ.", "Dạ, cháu mở Kinh A Di Đà cho bà đây ạ."

Định dạng JSON bắt buộc:
{
  "action_type": "PLAY_LIVE_TV" | "PLAY_CONTENT" | "SEARCH_YOUTUBE" | "SYSTEM_CONTROL" | "CLARIFY",
  "target": "vtv1 | volume_up | volume_down | sleep | pause | home | back",
  "content_id": "ID từ danh mục ứng viên nếu có, hoặc null",
  "query": "từ khóa tìm kiếm nếu không có trong danh mục",
  "feedback": "Dạ, cháu...",
  "confidence": 0.0 - 1.0
}
"""


class GeminiAIResolverAdapter(BaseAIResolverPort):
    def __init__(self, api_key: str = "", model_name: str = ""):
        self.api_key = (api_key or settings.GEMINI_API_KEY).strip()
        self.model_name = model_name or getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")

    def resolve(
        self,
        user_text: str,
        candidates: Optional[List[ContentItem]] = None,
        context_hints: Optional[Dict[str, Any]] = None
    ) -> ResolvedCommand:
        context_state = context_hints.get("state") if context_hints else None

        # Nếu chưa cấu hình API key chuẩn
        if not self.api_key or not self.api_key.startswith("AIzaSy"):
            return self._fallback_resolve(user_text, candidates, context_state)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

        candidate_info = []
        if candidates:
            for c in candidates:
                candidate_info.append(f"- ID: {c.id} | Tên: {c.name} | Thể loại: {c.category} | Diễn giả: {c.speaker_or_artist or 'Không'}")
        candidate_text = "\n".join(candidate_info) if candidate_info else "Không có ứng viên cụ thể."

        prompt = f"""Khẩu ngữ của ông bà: "{user_text}"

Danh sách ứng viên khả dụng từ hệ thống:
{candidate_text}

Ngữ cảnh trước đó: {context_hints or {}}

Hãy phân tích và trả về duy nhất định dạng JSON chuẩn:"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text_content = res_data["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text_content)

                act_str = data.get("action_type", "UNKNOWN")
                try:
                    act_type = TVActionType(act_str)
                except ValueError:
                    act_type = TVActionType.SEARCH_YOUTUBE

                cid = data.get("content_id")
                # Kiểm tra an toàn: nếu LLM tự sinh ID không có trong danh sách candidates, hủy bỏ
                if cid and candidates and not any(c.id == cid for c in candidates):
                    cid = None

                return ResolvedCommand(
                    action_type=act_type,
                    target=data.get("target", ""),
                    content_id=cid,
                    query=data.get("query", ""),
                    feedback=data.get("feedback", "Dạ, cháu đang xử lý cho ông bà ạ."),
                    confidence=float(data.get("confidence", 0.95)),
                    raw_text=user_text
                )
        except Exception:
            return self._fallback_resolve(user_text, candidates, context_state)

    def _fallback_resolve(
        self,
        user_text: str,
        candidates: Optional[List[ContentItem]] = None,
        context_state: Any = None
    ) -> ResolvedCommand:
        """
        Bộ phân giải ngữ nghĩa cục bộ thông minh (Single Source of Truth với SystemIntentClassifier).
        Chạy Offline hoặc dự phòng khi chưa cấu hình Cloud Gemini.
        """
        # 1. Kiểm tra lệnh hệ thống qua SystemIntentClassifier
        sys_cmd = SystemIntentClassifier.classify(user_text, context_state=context_state)
        if sys_cmd is not None:
            return sys_cmd

        text_lower = user_text.lower().strip()

        # 2. Kiểm tra xem có trùng khớp với ứng viên nào trong Catalog không
        if candidates:
            # So khớp chính xác hoặc có tên trong câu nói
            for c in candidates:
                if c.name.lower() in text_lower or (c.speaker_or_artist and c.speaker_or_artist.lower() in text_lower):
                    return ResolvedCommand(
                        action_type=TVActionType.PLAY_CONTENT,
                        target=c.deep_link or "",
                        content_id=c.id,
                        feedback=f"Dạ, cháu mở {c.name} cho bà đây ạ.",
                        confidence=0.95,
                        raw_text=user_text
                    )

            # Nếu nhắc tới từ khóa chung (Kinh, Phật, Cải lương...) mà có nhiều ứng viên
            matched_cat = []
            if any(w in text_lower for w in ["kinh", "phật", "pháp"]):
                matched_cat = [c for c in candidates if c.category == "BUDDHIST"]
            elif any(w in text_lower for w in ["cải lương", "tuồng", "vở"]):
                matched_cat = [c for c in candidates if c.category == "TRADITIONAL_MUSIC"]

            if len(matched_cat) >= 2:
                c1, c2 = matched_cat[0], matched_cat[1]
                return ResolvedCommand(
                    action_type=TVActionType.CLARIFY,
                    feedback=f"Dạ, bà muốn nghe {c1.name} hay {c2.name} ạ?",
                    confidence=0.75,
                    raw_text=user_text,
                    clarification_options=[c1.name, c2.name]
                )
            elif len(matched_cat) == 1:
                item = matched_cat[0]
                return ResolvedCommand(
                    action_type=TVActionType.PLAY_CONTENT,
                    target=item.deep_link or "",
                    content_id=item.id,
                    feedback=f"Dạ, cháu mở {item.name} cho bà nghe ạ.",
                    confidence=0.9,
                    raw_text=user_text
                )

        # 3. Nếu là câu lệnh tìm kiếm tự do trên YouTube
        clean_query = re.sub(
            r"^\s*(?:mở\s+youtube\s+tìm|tìm|bật|mở|nghe|xem)\s+",
            "",
            text_lower
        ).strip()
        # Loại bỏ các từ đuôi như "trên youtube", "cho bà", "đi cháu"
        clean_query = re.sub(
            r"\s+(?:trên\s+youtube|cho\s+(?:ông|bà|tôi)|đi(?:\s+cháu)?|với)\s*$",
            "",
            clean_query
        ).strip()

        if not clean_query:
            clean_query = user_text

        return ResolvedCommand(
            action_type=TVActionType.SEARCH_YOUTUBE,
            query=clean_query,
            feedback=f"Dạ, cháu đang tìm '{clean_query}' cho ông bà trên YouTube ạ.",
            confidence=0.9,
            raw_text=user_text
        )
