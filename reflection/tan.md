# Reflection — Dương Minh Tân

1. **Vai trò + phần mình làm:**
   Phụ trách dữ liệu, công cụ tra bài, impact và chi phí; reviewer và người merge cùng Hùng.
   Dữ liệu + công cụ: 3 bài synthetic (24 đoạn có mã) ở `data/lessons/`, `search_lesson` / `get_passage` ở `codebase/tools.py`, `data/DATA_CARD.md` (#52); sửa `search_lesson` giữ đoạn của ý thứ hai và xử lý câu hỏi dài tự nhiên (#58).
   Impact: dòng [J] trong `evidence/scripts/count_preclass.py` → 98/1.075 = 9,1% câu thiếu ngữ cảnh ở `spec.md` §2 (#53).
   Chi phí: 4 persona từ data pre-class và giá 3 model ở `cost/personas.yaml` (#26). Demo: trang `web/` hỏi thử, có chế độ phát lại khi mất mạng (#72).

2. **AI hỗ trợ mình thế nào:**
   Dùng Claude Code (Claude Opus 5.5) để viết bài synthetic theo hợp đồng chung, viết `search_lesson` (từ khoá + idf), script đếm data pre-class và trang `web/`.
   Phải sửa lại output AI: phân hạng khi bằng điểm dùng `find()` trả -1 nên xếp sai; `min()` lỗi trên danh sách rỗng; tiếng Việt vỡ trên console Windows; từ không có trong bài nào được idf lớn nhất nên lấn át từ khác (#58).
   Ở #72, Hùng review bắt được `server.py` và `make_replay.py` gọi thẳng `search_lesson`, nên trang hiện thiếu đoạn so với những gì model nhận ở câu nhiều vế → đổi sang `_search` của agent.
   Bài học: code AI viết phải có assert tự kiểm (`python codebase/tools.py`) và chạy trên chính câu thử của nhóm, không chỉ đọc lướt.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   B30 — *"Khi nào thì cần nhiều Agent hay RAG ạ?"*. Lượt 1 model hỏi lại lửng lơ, hứa "sẽ trả lời theo phần đó" nhưng không trả lời phần RAG, dù `search_lesson` đã lấy được `[D07-L1-P01]` (`eval/report.md` mục 2).
   Liên quan trực tiếp phần mình: ở #58 mình chỉ đo độ phủ là "có tìm ra đoạn không" (23/24 câu, `DATA_CARD.md`), nhưng tìm ra đoạn chưa đủ để câu trả lời đạt.
   Lỗi thật ở chỗ prompt coi "A hay B" là câu mơ hồ và chưa tra riêng từng vế; sửa ở #68 (`spec.md` §10), lượt 2 đạt 30/30.
   Học được: công cụ tra cứu phải đánh giá cùng cả luồng đầu–cuối, và câu thật của người dùng (B24–B30) bắt được lỗi mà câu nhóm tự đặt không bắt được.
