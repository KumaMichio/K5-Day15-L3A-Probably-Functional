"""Trang demo: hỏi thử trợ giảng + xem luồng ①→⑤ của từng câu.

Chạy:  python web/server.py            → mở http://127.0.0.1:8000/
       python web/server.py --port 8080

Chỉ thêm lớp web quanh answer() trong codebase/agent.py — không sửa khung, eval, simulate.
Không chạy server (mở thẳng web/index.html) thì trang tự về chế độ phát lại lượt 1.
"""
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

WEB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(WEB), "codebase"))

import tracing  # noqa: E402  (cần sys.path ở trên)
from agent import answer  # noqa: E402
from ai import MODEL_NAME, MODEL_PROVIDER  # noqa: E402
from tools import get_passage, search_lesson  # noqa: E402

MAX_QUESTION = 1000  # ký tự; câu dài hơn bị cắt để không gửi prompt quá lớn


def _event(e):
    """Giữ phần trang cần, bỏ prompt hệ thống (input của model) cho gọn."""
    keep = ("kind", "name", "text", "model", "tokens_in", "tokens_out", "latency_s", "error", "t")
    return {k: e[k] for k in keep if k in e}


def ask(question):
    question = (question or "").strip()[:MAX_QUESTION]
    tracing.begin("web")
    try:
        output = answer(question)["output"]
    except Exception as e:  # lỗi gọi model: báo lên trang, không sập server
        tracing.end()
        return {"error": "%s: %s" % (type(e).__name__, e)}
    summary, events = tracing.end()
    searched = any(e["kind"] == "tool" and e.get("name") == "search_lesson" for e in events)
    # gọi lại ngoài trace để có đủ đoạn + score (trace chỉ giữ 300 ký tự đầu); search_lesson chỉ đọc file, kết quả giống hệt
    passages = search_lesson(question) if searched else []
    return {"output": output, "events": [_event(e) for e in events], "summary": summary, "passages": passages}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB, **kwargs)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/health":
            return self._json({"ok": True, "provider": MODEL_PROVIDER, "model": MODEL_NAME or "fake"})
        if url.path == "/api/passage":
            code = (parse_qs(url.query).get("code") or [""])[0]
            p = get_passage(code)
            return self._json(p or {"error": "không có đoạn %s" % code}, 200 if p else 404)
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/ask":
            return self._json({"error": "không có đường dẫn này"}, 404)
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 64 * 1024)
            q = json.loads(self.rfile.read(length).decode("utf-8") or "{}").get("q", "")
        except (ValueError, AttributeError):
            return self._json({"error": "dữ liệu gửi lên không phải JSON {\"q\": \"...\"}"}, 400)
        self._json(ask(q))

    def log_message(self, fmt, *args):  # in gọn, không in nội dung câu hỏi
        sys.stderr.write("%s %s\n" % (self.command, urlparse(self.path).path))


def main():
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8000
    # HTTPServer một luồng: tracing giữ trạng thái chung, nên xử lý từng câu một
    server = HTTPServer(("127.0.0.1", port), Handler)
    print("Trang demo: http://127.0.0.1:%d/  ·  model: %s (%s)  ·  Ctrl+C để dừng"
          % (port, MODEL_NAME or "giả", MODEL_PROVIDER))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
