# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.
>
> **Khung slide:** [`slides/deck.html`](deck.html) — 9 trang đúng bảng dưới. Ô vàng = chờ số từ việc khác, thay hết trước khi xuất. Xuất: mở bằng Chrome → Ctrl+P → Lưu dưới dạng PDF · Lề: Không · bật Đồ hoạ nền → `demo-slides.pdf`.
> Mỗi người gửi số phần mình cho Huệ **trước 10:30 T7** (Tân: impact + chi phí · Thành: lượt 1, lượt 2, lỗi chính · Hùng: sơ đồ §4, 2 câu demo, link video).

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☑ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☑ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☑ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Một cải tiến** | Trước → Sau trên câu B30 (lượt 1 trượt, lượt 2 đạt) · đã sửa gì · kết quả 29/30 → 30/30 · đánh đổi | `eval/report.md` mục 3, `eval/run-1.csv`, `eval/run-2.csv` | ☑ |
| 7 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☑ |
| 8 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6, 7 | — | ☑ |
| 9 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

*Đề xuất theo phần mỗi người phụ trách — chốt khi tập demo 12:30 T7:*

| Trang | Người nói |
|---|---|
| 1 Người dùng & pain | Huệ |
| 2 Vì sao chọn bài này | Tân |
| 3 Giải pháp · 4 Demo live | Hùng |
| 5 Đánh giá thế nào · 6 Một cải tiến | Thành |
| 7 Chi phí khi dùng thật | Tân |
| 8 Kết luận · 9 Nếu có thêm 1 tuần | Hùng |
