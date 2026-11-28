# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py` (workflow 5 bước, kiểm mã đoạn) và `codebase/ai.py` (gọi OpenRouter / Anthropic, thử lại khi lỗi tạm thời) theo thiết kế ở `spec.md` §4 | Chạy `eval --try` và gọi thật từng câu khó trước khi merge; duyệt PR #51, #61, #63, #68 | Phan Sỹ Hùng |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn prompt hệ thống (4 quyết định, câu hỏi là dữ liệu) và lần cải tiến trước lượt 2 (câu hỏi hai vế) | Thử trên model thật 10 câu trước khi chạy lượt 2; ghi thay đổi ở `spec.md` §10 | Phan Sỹ Hùng |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Viết `evidence/scripts/count_preclass.py` đếm số tổng hợp trên `data/preclass/` | Chạy lại script, đối chiếu số với file CSV; kiểm tay __ dòng, khớp __ | Dương Minh Tân |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Video demo dự phòng | Claude Code + Playwright | Viết script điều khiển Chrome hỏi 4 câu trên trang `web/` (server thật, model thật), quay một lần không cắt; dải phụ đề do script dán lên trang, không đổi câu trả lời | Xem ảnh chụp sau từng câu trả lời, sửa phụ đề chi phí cho đúng ("/ phiên hỏi thành công"), tự đăng YouTube "Không công khai" | Phan Sỹ Hùng |
| Slide, văn bản | Claude Code | Dựng repo từ khung; soạn nháp `canvas.md`, `evidence/hypothesis.md`, `spec.md` §0–§2, `TEAMS.md` | Cả nhóm đọc lại, sửa lát cắt / pain cho khớp ý nhóm trước CP1 | Phan Sỹ Hùng |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
