# Quay video demo 30 giây (CP3 · video dự phòng CP4)

Quay **e2e thật**: Chrome tự động → `web/server.py` → `answer()` → model trong `.env`. Không cắt giữa, chỉ bỏ đoạn tải trang ở đầu.
Kịch bản: 1 câu thường (trả lời kèm mã đoạn, bấm mở đoạn) + 1 câu khó (chèn lệnh → AI chọn từ chối). `record.mjs` dừng nếu server đang ở model giả.

Cần: Node, Python, ffmpeg trong PATH, Chrome (đường dẫn khác thì đặt biến `CHROME`). Giọng đọc (không bắt buộc): OmniVoice.

```
# 1 · bật server bằng model thật (cửa sổ khác)
python web/server.py
# 2 · quay + khung đầu/cuối   (cd web/demo)
npm install && npx playwright-core install ffmpeg
node record.mjs http://127.0.0.1:8000/ out
node cards.mjs  http://127.0.0.1:8000/ out "<tên model trong .env>"
python build.py plan out                       # → out/timeline.json
# 3 · giọng đọc tiếng Việt (môi trường riêng, CPU chạy được)
python -m venv ovenv && ovenv/Scripts/pip install omnivoice   # macOS/Linux: ovenv/bin/pip
ovenv/Scripts/python voice.py out/timeline.json out            # lần đầu tải model k2-fsa/OmniVoice
# 4 · ghép
python build.py video out out demo.mp4         # không giọng đọc: python build.py video out - demo.mp4
```

Đoạn quay dài quá 27,5 giây (model chậm) thì `build.py` báo — quay lại. Video đẩy YouTube "Không công khai" hoặc Drive "Bất kỳ ai có đường liên kết", mở thử bằng cửa sổ ẩn danh. **Không commit** `out/`, `*.mp4`.
