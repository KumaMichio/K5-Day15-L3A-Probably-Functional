# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ 9 phép đếm x/N, script `evidence/scripts/count_preclass.py`, 7 ví dụ | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ đang hẹn (câu hỏi: `evidence/interviews/questions.md`) | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **đạt**: 28 phiếu, 23 đúng vai (17 học viên L3A, 6 L3B); 5 phiếu TA / khác bị loại | `evidence/survey/results.csv` (đã ẩn danh) · đếm: `evidence/survey/summarize.py` |

## 2. Số chính

- Đào data (05–25/11/2026, `evidence/data-mining.md` mục 3):
  - 98/1.075 câu trả lời của trợ giảng (9,1%) bị tự gắn cờ thiếu ngữ cảnh — **97/98 vẫn trả lời dài ≥100 ký tự**.
  - 231/557 câu trả lời từ 13/11 (41,5%) không dẫn mốc nào trong bài.
  - 530/1.090 câu hỏi (48,6%) được hỏi tiếp cùng video trong 3 phút hoặc tua lùi trong 2 phút — tín hiệu yếu.
  - 145/436 học viên có hoạt động (33,3%) từng nhắn AI — 2/3 chưa dùng.
- Phỏng vấn: __/3 người gặp *(n nhỏ không ghi %)* · số lần / tháng: P1 __, P2 __, P3 __ · mỗi lần mất __–__ phút
- Khảo sát (form 27/11/2026, n = 23 học viên L3 ngoài nhóm; chạy lại: `python evidence/survey/summarize.py <export.csv>`):
  - 14/23 (60,9%) gặp chỗ chưa hiểu trong lần xem gần nhất · lần đó mất: dưới 5 phút 6/23 · **5–15 phút 11/23 (47,8%)** · 15–30 phút 2/23 · trên 30 phút 1/23 · không nhớ 3/23.
  - Cuối cùng: hiểu 6/23 · **hiểu một phần 13/23 (56,5%)** · bỏ qua 2/23 · **vào lớp mới thấy hiểu sai 2/23**.
  - Đã làm gì (chọn nhiều): **hỏi ChatGPT / AI ngoài 14/23 (60,9%)** · hỏi trợ giảng dưới video 11/23 · hỏi bạn 11/23 · bỏ qua 9/23 · tua lại 7/23 · Google 6/23 · Discord 5/23.
  - Trong 16 người không chọn "chưa từng hỏi trợ giảng": **13/16 sau khi đọc câu trả lời vẫn không chắc, hoặc phải hỏi chỗ khác / tua lại để kiểm** (hỏi chỗ khác 9/16 · không chắc nhưng vẫn xem tiếp 8/16 · tua lại 3/16).
  - Kiểm câu trả lời của trợ giảng bằng cách nào (17 câu tự do): 9/17 hỏi AI khác (ChatGPT, Claude…) hoặc Google · 1/17 xem lại bài giảng cũ · không ai kể là mở đúng đoạn trong bài.
  - **Chất lượng phiếu:** 4 phiếu (#05, #08, #12, #25) chọn "chưa từng hỏi trợ giảng" cùng lúc với các việc làm sau khi hỏi; 3 phiếu (#03, #16, #22) chưa xem video bao giờ; 2 phiếu (#04, #09) chọn cả "hiểu luôn" và "không chắc". Không sửa phiếu — chỉ báo con số kèm giới hạn này.

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

*Data không có câu chữ, chỉ có độ dài — mục 1–5 là ví dụ hành vi từ data (`evidence/data-mining.md` mục 4). Mục 6–10 trích nguyên văn câu trả lời tự do của khảo sát, số phiếu = thứ tự dòng trong `evidence/survey/results.csv`. Trích từ P1–P4 thêm vào sau.*

1. `C00983` · `Day01/d01-r1-v05` · hỏi 29 ký tự → trợ giảng tự gắn thiếu ngữ cảnh nhưng vẫn trả lời 182 ký tự — dòng data `C00983`
2. `C00676` · `Day01/d01-r1-v01` · hỏi 48 ký tự → thiếu ngữ cảnh, vẫn trả lời 359 ký tự — dòng data `C00676`
3. `C01187` · `Day06/d06-r1-v01` · hỏi 92 ký tự → trả lời 600 ký tự, không dẫn mốc nào trong bài — dòng data `C01187`
4. `C00581` · `Day01/d01-r1-v02` · nhận 388 ký tự → hỏi tiếp cùng video sau 61 giây — dòng data `C00581`
5. `C00979` · `Day01/d01-r1-v01` · nhận 333 ký tự → tua lùi video trong 2 phút — dòng data `C00979`
6. "Kiến thức về chủ đề đó khá là mới và AI cũng chưa có nguồn nào chính thống để kiểm tra." — phiếu khảo sát #07 (học viên L3A)
7. "không biết đúng hay sai" — phiếu khảo sát #21 (học viên L3B)
8. "chưa tự xác nhận được" (điều khó chịu nhất) · kiểm bằng cách: "Vào lớp mới thấy mình hiểu sai" — phiếu khảo sát #15 (học viên L3A)
9. "Mất thời gian để đi confirm lại thông tin" — phiếu khảo sát #26 (học viên L3B)
10. "lên các nền tảng AI kiểm tra cũng như tài liệu bài giảng trên mạng" — phiếu khảo sát #07 (học viên L3A)
11. "đọc khó hiểu phải đi tìm nguồn đúng để đọc hiểu" — phiếu khảo sát #23 (học viên L3A)
12. "…" — P_ *(chờ phỏng vấn)*

## 4. Các nguồn có khớp nhau không

Data nói trợ giảng trả lời cả khi thiếu căn cứ (97/98) và 41,5% câu không chỉ ra mốc nào, nhưng không cho biết học viên có khó chịu không; khảo sát (23 học viên) nói 13/16 người đã hỏi trợ giảng vẫn không chắc hoặc phải kiểm ở chỗ khác, và cách kiểm phổ biến là hỏi AI khác (9/17) — không ai kể mở đúng đoạn bài. **Khớp:** data cho thấy câu trả lời thường không có mốc để tự kiểm (41,5%); người dùng nói họ không tự xác nhận được và tốn thời gian xác minh. **Lệch / chưa rõ:** data E/G (48,6% hỏi tiếp / tua lại) là tín hiệu yếu, khảo sát cho thấy tua lại để kiểm ít (3/16) — học viên kiểm bằng AI ngoài nhiều hơn tua video. Khảo sát có phiếu mâu thuẫn, nên cần phỏng vấn để nghe chuyện cụ thể. *(chờ P1–P4)*

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng / sai / phải đổi** — vì __. Điều vẫn chưa biết: __

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| | | |
