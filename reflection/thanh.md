# Reflection — Nguyễn Bá Thành

1. **Vai trò + phần mình làm:**
   Mình ở cặp Y (bằng chứng + đánh giá), phụ trách định nghĩa "tốt", kịch bản chỗ khó và toàn bộ bộ đánh giá của nhóm (`spec.md` §5 & §7, `eval/metric_spec.yaml`, `eval/benchmark.csv`, `eval/cham-cheo.md`, `eval/README.md`, `eval/report.md` — PR #55, #57, #60, #66, #71).
   Thiết kế lưới độ phủ 4 chiều cho 30 câu thử (`11 thuong · 15 kho · 4 tu_choi`, trong đó `10/30` câu từ 7 câu hỏi nguyên văn của 4 học viên L3 ngoài nhóm dưới video và 3 dòng chat 1–2 ký tự trong `data/preclass/chat.csv`), chốt 4 metric (chấm chéo khớp 5/5 với Huệ) và chuẩn "đạt" trước giờ khoá CP2 19:30.
   Trực tiếp chấm tay cột `pass` và `ghi_chu` cho cả hai lượt chạy trên Claude Haiku 5.5 (`eval/run-1.csv` đạt 29/30 ở #64; `eval/run-2.csv` đạt 30/30 ở #69), phân tích nhóm lỗi để nhóm chọn cải tiến ở #32 và trình bày phần Đánh giá khi demo.

2. **AI hỗ trợ mình thế nào:**
   Dùng coding agent (Antigravity) để rà độ phủ các kịch bản chỗ khó, kiểm tra nhanh điểm từ khoá của câu thử trên `search_lesson` và tổng hợp bảng đối chiếu `run-1.csv` → `run-2.csv`.
   Phải tự kiểm và sửa lại output của AI ở hai điểm lớn: (1) bản nháp đầu (#55) AI gán nhãn `data_that` cho các câu tự viết mô phỏng hành vi từ `chat.csv` trong khi file gốc không lưu chữ câu hỏi — sau khi Hùng và Tân góp ý, mình đổi về `tu_viet` trung thực và trực tiếp đi thu 7 câu hỏi nguyên văn của học viên L3 ngoài nhóm (`B24`–`B30`); (2) chỉnh câu tấn công `B12`, `B23` không chứa từ khoá làm hộ bài để vượt qua regex bước ①, thực sự kiểm được lớp chặn trong prompt ở bước ③.
   Bài học: AI sinh biến thể câu thử rất nhanh, nhưng tính xác thực của nhãn nguồn và việc câu thử có chạm đúng tầng rào chắn cần đo hay không thì người phụ trách bắt buộc phải tự kiểm bằng tay.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   `B30` — câu hỏi thật của học viên *"Khi nào thì cần nhiều Agent hay RAG ạ?"*, là câu duy nhất trượt ở lượt 1 (`eval/run-1.csv`). Dù `search_lesson` đã lấy được `[D07-L1-P01]`, model lại chọn `hoi_lai` (*"Bạn muốn hỏi về RAG hay nhiều Agent? … mình sẽ trả lời theo phần đó"*) trong khi hệ thống không lưu lịch sử hội thoại để trả lời ở lượt sau.
   Nguyên nhân: luật 4 trong prompt làm model nhầm câu so sánh `"A hay B"` là câu mơ hồ, đồng thời ở `B03` việc tra bài nguyên câu làm sót đoạn `[D07-L1-P01]` của vế hai (`eval/report.md` mục 2).
   Sau cải tiến #68 (tách vế tra thêm + sửa luật 3–4 ưu tiên trả lời phần có căn cứ và nói rõ phần ngoài bài), lượt 2 đạt 30/30, nhưng lộ rõ đánh đổi: câu dẫn nhập dài `B06` giải thích thừa bối cảnh `D01-L1-P06` và token vào trung bình tăng 21% (`665 → 804`).
   Học được: 20 câu tự đặt của nhóm đều qua, chỉ câu nguyên văn của người dùng thật mới làm lộ chỗ xung đột giữa hai quy tắc trong prompt; và mỗi lần sửa lỗi luôn phải đo lại trọn bộ để thấy cái giá về độ gọn và chi phí.
