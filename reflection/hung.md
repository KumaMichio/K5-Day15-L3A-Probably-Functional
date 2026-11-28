# Reflection — Phan Sỹ Hùng

1. **Vai trò + phần mình làm:**
   Đội trưởng: chốt Track A (A1), chia 15 việc theo hạn nội bộ (`plan/index.html`, luật git ở `CLAUDE.md`, #45), duyệt và merge PR, nộp cả 4 checkpoint (#2).
   Code: thiết kế luồng cố định ①→⑤ ở `spec.md` §4 và `codebase/agent.py` (#51), nối model thật Claude Haiku 5.5 qua OpenRouter + chặn rủi ro trong `codebase/ai.py` (#61, #63), tra thêm từng vế cho câu hỏi nhiều vế (#68).
   Chạy lượt 1, lượt 2 (#64, #69) và mô phỏng chi phí `simulate-1`; viết `spec.md` §6, §9, §10 (#62, #65, #70), README (#67, #73) và quay video demo dự phòng.

2. **AI hỗ trợ mình thế nào:**
   Dùng Claude Code (Claude Opus 5.5) để viết code `agent.py` / `ai.py` và prompt, đọc lại PR của bạn, soạn nháp spec, chữ nộp form và kịch bản demo; khai báo ở `docs/ai-usage.md`.
   Phải sửa lại output AI ở mấy chỗ: bản tách câu hỏi theo vế đầu tiên kéo nhầm đoạn bài không liên quan vào B09 → thêm điều kiện chỉ nhận đoạn có chung từ chủ đề hiếm (`TOPIC_DF`); số điểm B03 trong báo cáo phải tính lại bằng `tools.py` vì trace bị cắt 300 ký tự; chú thích video ghi nhầm $0.00057 là "mỗi câu hỏi" trong khi đó là "mỗi phiên thành công" → quay lại.
   Bài học: AI viết nhanh, nhưng số nào AI đưa ra mình vẫn phải truy về file lượt chạy trước khi đưa vào spec.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   B30 — câu thật của học viên *"Khi nào thì cần nhiều Agent hay RAG ạ?"*. Lượt 1 model chọn `hoi_lai` lửng lơ: hỏi lại "RAG hay nhiều Agent", hứa "sẽ trả lời theo phần đó" nhưng không trả lời phần RAG kèm `[D07-L1-P01]` (`eval/run-1.csv`).
   Nguyên nhân: tra bài bằng cả câu chỉ ra đoạn của vế chiếm nhiều từ, và luật trong prompt chưa nói gì về câu hỏi một nửa trong bài, một nửa ngoài bài.
   Sửa ở #68: tra thêm từng vế, prompt dặn trả lời phần có căn cứ và nói rõ phần còn lại không có trong bài; lượt 2 đạt 30/30. Đánh đổi: token vào tăng ~21% và B06 dài dòng hơn.
   Học được: câu hỏi thật của học viên hay ghép nhiều ý, nên bộ câu thử cần câu từ data thật, không chỉ câu nhóm tự nghĩ ra.
