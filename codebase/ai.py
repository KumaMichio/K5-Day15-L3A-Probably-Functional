"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call, note

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường
RETRY_STATUS = (429, 500, 502, 503, 504, 529)   # lỗi tạm thời: thử lại, không phải lỗi của mình
MAX_RETRIES = 2


def _retry_wait(header, attempt):
    """Số giây chờ trước khi thử lại. retry-after có thể là số giây hoặc ngày giờ (HTTP-date);
    không đọc được thì chờ 2, 4 giây. Giới hạn 30 giây để eval không treo lâu."""
    fallback = 2 * (attempt + 1)
    if not header:
        return fallback
    try:
        return min(max(float(header), 0.0), 30.0)
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime
        from datetime import datetime, timezone
        delta = (parsedate_to_datetime(header) - datetime.now(timezone.utc)).total_seconds()
        return min(max(delta, 0.0), 30.0)
    except (TypeError, ValueError):
        return fallback


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib).
    Lỗi tạm thời (429 hết lượt, 5xx, 529 quá tải) thử lại tối đa MAX_RETRIES lần, chờ theo retry-after.
    Lỗi khác (400 sai tham số, 401 sai key) báo ngay để khung ghi vào cột error."""
    data = json.dumps(body).encode("utf-8")
    for attempt in range(MAX_RETRIES + 1):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in RETRY_STATUS and attempt < MAX_RETRIES:
                time.sleep(_retry_wait(e.headers.get("retry-after"), attempt))
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(out, ensure_ascii=False, indent=2)[:3000])
    return out


# --- Claude (Anthropic Messages API) ---------------------------------------------------------------
# Model nhóm dùng: Claude Haiku 5.5 — MODEL_NAME=claude-haiku-5-5 (bảng giá: further-reading/model-prices.md).
# - anthropic-version 2026-10-21: không gửi temperature / top_p / top_k (phiên bản này trả lỗi 400).
# - Haiku 5.5 bật suy nghĩ (adaptive thinking) mặc định; token suy nghĩ tính vào output_tokens và vào max_tokens,
#   nên max_tokens để rộng (4000) để JSON không bị cắt. effort "low": việc chỉ là chọn 1 trong 4 quyết định
#   từ ≤3 đoạn ngắn, không cần suy nghĩ sâu — rẻ và nhanh hơn mặc định "medium".
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
CLAUDE_VERSION = "2026-10-21"
CLAUDE_MAX_TOKENS = 4000
CLAUDE_EFFORT = "low"


def call_claude(system, user):
    data = post_json(URL_CLAUDE,
                     {"x-api-key": API_KEY, "anthropic-version": CLAUDE_VERSION},
                     {"model": MODEL_NAME, "max_tokens": CLAUDE_MAX_TOKENS, "system": system or "",
                      "output_config": {"effort": CLAUDE_EFFORT},
                      "messages": [{"role": "user", "content": user}]})
    # Chỉ lấy khối "text" (bỏ khối "thinking"). stop_reason khác end_turn (max_tokens, refusal) → ghi vào trace;
    # agent.py tự xử lý chữ hỏng / rỗng bằng đường "không chắc".
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    if data.get("stop_reason") not in ("end_turn", "stop_sequence"):
        note("model dừng: stop_reason=%s" % data.get("stop_reason"))
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


# --- OpenRouter (định dạng OpenAI chat/completions) -------------------------------------------------
# MODEL_NAME = slug của OpenRouter, chép đúng từ https://openrouter.ai/models (vd model Claude Haiku 5.5).
# Token lấy từ usage của phản hồi (prompt_tokens / completion_tokens). Bảng giá của đề không có dòng OpenRouter,
# nhưng giá Claude Haiku 5.5 trên OpenRouter (0.10 / 0.50 USD mỗi 1M token, xem https://openrouter.ai/api/v1/models
# ngày 28/11/2026) bằng giá Anthropic trong bảng → cost/ dùng thẳng giá trong bảng, ghi nguồn OpenRouter + ngày xem.
URL_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"


def call_openrouter(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENROUTER, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages, "max_tokens": CLAUDE_MAX_TOKENS})
    choice = data["choices"][0]
    if choice.get("finish_reason") not in ("stop", None):
        note("model dừng: finish_reason=%s" % choice.get("finish_reason"))
    u = data["usage"]
    return {"text": choice["message"].get("content") or "",
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if not API_KEY or not MODEL_NAME:
        raise RuntimeError("thiếu API_KEY hoặc MODEL_NAME trong .env — xem docs/connect-model.md mục 1")
    if MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "openrouter":
        r = call_openrouter(system, user)
    else:
        raise NotImplementedError(
            "chưa viết phần gọi model cho MODEL_PROVIDER=%s — dùng anthropic hoặc openrouter" % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
