# Reflection — Dương Thị Huệ

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình ở cặp Y (bằng chứng + đánh giá), phụ trách bằng chứng pain và slide.
   - **#8 (PR #49):** bộ câu hỏi phỏng vấn theo Mom Test (`evidence/interviews/questions.md`), Google Form khảo sát tạo bằng `evidence/survey/create_form.gs`, `spec.md` §1 (số khớp lát cắt 98/1.075 = 9,1%) và §3 (giải pháp tương tự: NotebookLM, Coursera Coach, Khanmigo), trích dẫn ở canvas dòng 4 cho CP2.
   - **#25 (PR #56):** khảo sát 23 học viên L3 ngoài nhóm (đạt ngưỡng ≥20), số chính là 13/16 người đã hỏi trợ giảng vẫn không chắc hoặc phải kiểm ở chỗ khác. Kết quả ẩn danh ở `evidence/survey/results.csv`, đếm bằng `evidence/survey/summarize.py`, tổng hợp ở `evidence/summary.md`.
   - **#36 (PR #50):** `slides/deck.html` → `demo-slides.pdf`, mỗi trang có số và nguồn. Sau CP4 mình thêm trang "Điểm mới so với trợ giảng hiện tại" và trang "Một cải tiến".
   - **Đánh giá:** đọc và chạy thử #51, #52, chỉ ra đường `tu_choi` không bao giờ chạy tới. Hùng sửa bằng cách chặn xin làm hộ bài ở bước ①. Chấm chéo 5 output mẫu, khớp 5/5 với Thành (#60).
   - **Chưa làm được:** phỏng vấn P1–P4 (#8 vẫn mở). Chỉ 1/23 người làm khảo sát đồng ý cho hỏi thêm, nên bằng chứng nghiêng về số đếm, thiếu chuyện cụ thể của từng người.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude Code để soạn nháp bộ câu hỏi, viết Apps Script tạo form, viết script đếm khảo sát, ghép số từ `eval/` và `cost/` vào slide, và ghép nhánh #51 với #52 để chạy thử trước khi góp ý.
   - Chỗ phải sửa: script đếm ban đầu tách câu chọn nhiều theo ", ", nhưng file CSV tải từ Google Form nối bằng ";". Lỗi này lộ ra ở các dòng "Khác: ;;;", phải sửa rồi đếm lại.
   - Số trong spec §1 và canvas cũng phải cập nhật từ 17 lên 23 người, vì #49 đã merge trước khi có thêm phiếu.
   - Slide bản đầu AI dựng đủ số nhưng để phần cải tiến và điểm mới chìm trong hai dòng chữ nhỏ. Mình phải yêu cầu tách thành trang riêng có Trước → Sau.
   - Điều mình rút ra: AI không thay được phần cần người thật. Nó từ chối chép câu trả lời khảo sát sang file phỏng vấn, và nhắc mình rằng số khảo sát có phiếu mâu thuẫn thì phải ghi rõ, không được sửa.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Câu **B30** *"Khi nào thì cần nhiều Agent hay RAG ạ?"* là câu thật của học viên, và là câu duy nhất trượt ở lượt 1. Trợ giảng hỏi ngược lại rồi hứa *"mình sẽ trả lời theo phần đó"*, nhưng hệ thống không nhớ hội thoại nên lời hứa đó không bao giờ được thực hiện.
   - Câu tự viết của nhóm đều đạt. Phải đến câu của người dùng thật mới lộ ra kiểu hỏi so sánh hai vế, mà kiểu này rất tự nhiên khi đang xem video.
   - Nó cũng khớp với khảo sát: 13/16 người đã hỏi trợ giảng vẫn phải kiểm ở chỗ khác, và một câu trả lời nửa vời đủ làm học viên quay sang ChatGPT.
   - Mình học được hai điều. Bộ câu thử cần có câu nguyên văn của người dùng ngay từ đầu, đó là lý do nên phỏng vấn sớm hơn. Và "trả lời được một phần, nói rõ phần không có" có ích hơn hỏi lại. Sau cải tiến #68, B30 đạt ở lượt 2.
